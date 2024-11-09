#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# constants #################################################################

DATA_UNIT, PALETTE_UNIT = range(2)  # texture unit use


# common shaders ############################################################

VERT_SHADER = r"""
    #version 330

    uniform mat4 model_matrix;
    uniform mat4 view_matrix;
    uniform mat4 projection_matrix;

    layout (location = 0) in vec3 vertex;
    layout (location = 1) in vec2 tex_coord;

    out vec2 tex_coord0;

    void main() {
        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex, 1.);
        tex_coord0 =  tex_coord;
    }
"""

PALETTE_SHADER = r"""
    #version 330

    // handling values
    uniform sampler2D values;

    in vec2 tex_coord0;

    vec2 v() {
        // compute original value, keep alpha for nans
        vec4 t = texture(values, tex_coord0);
        return t.xy;
    }

    // handling palette
    uniform sampler1D palette;

    uniform float v0; // lower and
    uniform float v1; // upper bound of data values mapped to the palette

    vec4 colormap(float v) {
        return texture(palette, (v-v0)/(v1-v0));
    }
"""

ALPHA_SHADER = r"""
    #version 330

    uniform float alpha;

    vec4 apply_alpha(vec4 color) {
        return vec4(color.rgb, color.a*alpha);
    }
"""

# Map fragment shaders ######################################################

MAP_SHADER = r"""
    #version 330

    vec2 v();
    vec4 colormap(float v);
    vec4 apply_alpha(vec4 color);

    in vec2 tex_coord0;
    out vec4 frag_color;

    void main() {
        // retrieve original value, and color code
        vec2 v = v();
        if(v.y < 0.5) { discard; }
        vec4 l = colormap(v.x/v.y);
        frag_color = apply_alpha(vec4(l.rgb, 1.));
    }
"""

GEOMAP_SHADER = r"""
    #version 330

    vec4 apply_alpha(vec4 color);

    uniform sampler2D geomap_texture;

    in vec2 tex_coord0;
    out vec4 frag_color;

    void main() {
        frag_color = apply_alpha(texture(geomap_texture, tex_coord0));
    }
"""

# MiniMapView shaders for MapView viewport rect ####################################################

VIEWPORTRECT_VERT_SHADER = r"""
    #version 330

    uniform mat4 model_matrix;
    uniform mat4 view_matrix;
    uniform mat4 projection_matrix;

    layout (location = 0) in vec3 vertex;

    void main() {
        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex, 1.);
    }
"""

VIEWPORTRECT_FRAG_SHADER = r"""
    #version 330

    uniform vec4 rect_color;

    out vec4 frag_color;

    void main() {
        frag_color = rect_color;
    }
"""
