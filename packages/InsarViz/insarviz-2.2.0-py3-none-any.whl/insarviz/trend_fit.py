#!/usr/bin/env python3
# developped by Romain Montel


"""
The model chosen to represent the surface displacements comes from this publication:
Fourteen-Year Acceleration Along the Japan Trench, 10.1029/2020JB021226, page 5

The model has:
-a linear component: xr+v(t-tr), xr the reference position, v the initial velocity, tr the reference time (1997/01/01)

-a seasonal component: s1*sin(2pi(t-tr))+c1*cos(2pi(t-tr))+s2*sin(4pi(t-tr))+c2*sin(4pi(t-tr))

-an earthquake component: sum of mi*H(t-ti),
 mi is the amplitude of transients for each seismic and ti the starting time of the seismic
 H(t-ti) equal to 0 if t<ti and 1 if t>=ti
 for earthquake with post seismic you have to multiply the earthquake component by log(1+(t-ti)/Tr
 Tr is the characteristic time of the post seismic, the default value is 100 days

-a slow deformation component: sum of ds*J(t-ts)
 ds is the amplitude for each slow deformation and ts the starting time of the slow deformation
 J(t-ts) equal to 0 if t<ts, to -1/2*cos(pi*tnorm)+1/2 if ts<=t<=ts+td, to 1 if t>ts+td,
 td is the duration of the slow deformation events, and tnorm=(t-ts)/td

Algorithm:
==========

The purpose of the algorithm is to determine the value of the following parameters: xr, v, s1, c1, s2, c2, mi, ds

Examples:
=========
curve_fit -c 1891:4297 -f "D:/data_insarviz/CNES_DTs_geo_8rlks_cog.tiff" -l -s -e 100 2018/02/16 0 -p
"""

# classical imports
import argparse
import logging
import numpy as np
from pathlib import Path
import sys

import time

from insarviz.Loader import Loader

import multiprocessing
from multiprocessing import Pool
from functools import partial

import rasterio

import insarviz.cy_fit as cy_fit

logger = logging.getLogger(__name__)


def multi_trend_fit(arg, fit_mode, reference_time=(0,0,0), characteristic_time=100,
                    duration_time=[], post_seismic=[], earthquake_init_time=[], slow_deformation_init_time=[]):

    start_line, start_column, chunk_size, max_col, img_name = arg
    class_curve_fit = cy_fit.curve_fit_algorithm(fit_mode, reference_time, characteristic_time,
                                                 duration_time, post_seismic, earthquake_init_time,
                                                 slow_deformation_init_time)

    number_of_parameters = 8 + len(earthquake_init_time) + len(slow_deformation_init_time)

    class_curve_fit.load_date(img_name)
    res = np.zeros((chunk_size, max_col - start_column, number_of_parameters))
    for x in range(start_line, start_line + chunk_size):
        # print(f"{multiprocessing.current_process()} processing row  {x}")
        for y in range(start_column, max_col):
            class_curve_fit.load_data_band(x, y)
            if class_curve_fit.band.size == 0:
                res[x-start_line, y-start_column, :] = [0.0] * number_of_parameters
                continue
            class_curve_fit.fit(class_curve_fit.time_data[class_curve_fit.where_nan],
                                class_curve_fit.band,
                                np.ones(len(class_curve_fit.band)))
            res[x-start_line, y-start_column, :] = class_curve_fit.arg
    return res


def main():
    """
    The main stuff
    """
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Fit predefined curves given a set of points")
    parser.add_argument("-f", type=str, required=True, help="filename of the data")

    parser.add_argument("-c", type=str, default=None, help="to fit in one point, format: pos_x:pos_y")
    parser.add_argument("-w", type=str, default=None,
                        help="to fit on a windows of the cube, format: pos_x1:pos_y1:pos_x2:pos_y2")

    parser.add_argument("--start", type=int, default=0, help="index of the first date in time_data_array")
    parser.add_argument("--end", type=int, default=-1, help="index of the first date in time_data_array")

    parser.add_argument("-r", type=str, default="first_data", help="format: reference time yyyy/mm/dd (optionnal)")

    parser.add_argument("-l", action="store_true", help="add a linear trend in the function")
    parser.add_argument("-s", action="store_true", help="add a seasonal trend in the function")
    parser.add_argument("-a", action="store_true", help="add a acceleration trend in the function")

    parser.add_argument("-e", type=str, nargs=3,
                        help="add a earthquake trend in the function, format:"
                             "characteristic_time (number of days)"
                             "earthquake_time_list (separate by ':', date format: yyyy/mm/dd)"
                             "post_seismic_list (0 or 1 separated by ':')")
    parser.add_argument("-d", type=str, nargs=2,
                        help="add a slow deformation trend in the function, format:"
                             "duration_time list of days (separate by ':')"
                             "slow_deformation_time_liste (separate by ':', date format: yyyy/mm/dd)")

    parser.add_argument("-p", action="store_true", help="plot the result of the curve fit")

    parser.add_argument("-H", action="store_true",
                        help="provide more detailed help")
    parser.add_argument("-v", type=int, default=3,
                        help=("set logging level:"
                              "0 critical, 1 error, 2 warning,"
                              "3 info, 4 debug, default=info"))
    if "-H" in sys.argv:
        print(__doc__)
        return 0

    args = parser.parse_args(argv)

    logging_translate = [logging.CRITICAL, logging.ERROR, logging.WARNING,
                         logging.INFO, logging.DEBUG]
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging_translate[args.v])
    script_base_name = Path(__file__).name
    logger = logging.getLogger(script_base_name + ":main")
    cmd_line = ' '.join(sys.argv)
    logger.info(f"called as {cmd_line}")

    if args.e is not None:
        assert len(args.e[2].split(":")) == len(args.e[1].split(":")), "these two lists must have the same length"
    if args.d is not None:
        assert len(args.d[2].split(":")) == len(args.d[1].split(":")), "these two lists must have the same length"

    filename = args.f
    mode = ""

    if args.r != "first_data":
        reference_time = tuple([int(e) for e in args.r.split("/")])
    else:
        reference_time = (0, 0, 0)

    start_time = args.start
    end_time = args.end

    if args.l:
        mode += "l"
    if args.s:
        mode += "s"
    if args.a:
        mode += "a"

    if args.e is not None:
        mode += "e"
        characteristic_time = float(args.e[0])
        earthquake_time_list_temp = [e.split("/") for e in args.e[1].split(":")]
        earthquake_init_time = [tuple([int(i) for i in e]) for e in earthquake_time_list_temp]
        post_seismic_list = [bool(int(e)) for e in args.e[2].split(":")]
    else:
        characteristic_time = 0
        earthquake_init_time = []
        post_seismic_list = []

    if args.d is not None:
        mode += "j"
        duration_time = [float(e) for e in args.d[0].split(":")]
        slow_deformation_time_list_temp = [e.split("/") for e in args.d[1].split(":")]
        slow_deformation_init_time = [tuple([int(i) for i in e]) for e in slow_deformation_time_list_temp]
    else:
        duration_time = []
        slow_deformation_init_time = []

    # Todo weight and user function trend
    if args.c:

        class_curve_fit = cy_fit.curve_fit_algorithm(mode, reference_time, characteristic_time,
                                                     duration_time, post_seismic_list, earthquake_init_time,
                                                     slow_deformation_init_time)

        class_curve_fit.load_date(filename)

        coor = [float(e) for e in args.c.split(":")]
        class_curve_fit.load_data_band(*coor)

        class_curve_fit.fit(class_curve_fit.time_data[class_curve_fit.where_nan],
                            class_curve_fit.band, [1] * len(class_curve_fit.band), start_time, end_time)

        if args.p:
            class_curve_fit.plot(class_curve_fit.time_data[class_curve_fit.where_nan],
                                 class_curve_fit.band, class_curve_fit.arg, start_time, end_time)

        return class_curve_fit.arg

    elif args.w:
        windows = np.int32(args.w.split(":"))
        assert windows[0] < windows[2] and windows[1] < windows[3]
    else:
        windows = "all"

    number_of_parameters = 8 + len(earthquake_init_time) + len(slow_deformation_init_time)

    with rasterio.open(filename) as ds:
        if windows == "all":
            nb_lines = ds.width
            nb_cols = ds.height
        else:
            nb_lines = windows[2]
            nb_cols = windows[3]

        crs = ds.crs
        transform = ds.transform

    if windows == "all":
        start_line = 0
        start_column = 0
    else:
        start_line = windows[0]
        start_column = windows[1]

    nb_procs = multiprocessing.cpu_count()
    pas = (nb_lines - start_line) // nb_procs
    residu = (nb_lines - start_line) % nb_procs
    inputs = []

    while start_line < nb_lines:
        if residu == 0:
            inputs.append((start_line, start_column, pas, nb_cols, filename))
            start_line += pas
        else:
            inputs.append((start_line, start_column, pas + 1, nb_cols, filename))
            start_line += pas + 1
            residu -= 1

    nb_procs = multiprocessing.cpu_count()
    t0 = time.time()
    p = Pool(nb_procs)
    res = p.map(partial(multi_trend_fit, fit_mode=mode, reference_time=reference_time,
                        characteristic_time=characteristic_time,
                        duration_time=duration_time, post_seismic=post_seismic_list,
                        earthquake_init_time=earthquake_init_time,
                        slow_deformation_init_time=slow_deformation_init_time), inputs)

    res_array = np.concatenate(res)
    print(f"time for {nb_procs * pas}= {time.time() - t0} sec")
    # creating output
    start_line = windows[0]
    with rasterio.open('out.tiff', 'w', driver='GTiff',
                       height=nb_cols - start_column, width=nb_lines - start_line,
                       count=number_of_parameters, dtype=np.float32,
                       crs=crs, transform=transform) as new_dataset:
        for param_nb in range(number_of_parameters):
            new_dataset.write(res_array[:, :, param_nb].reshape((nb_lines - start_line, nb_cols - start_column)),
                              param_nb + 1)


if __name__ == "__main__":
    sys.exit(main())
