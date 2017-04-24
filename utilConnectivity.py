# -*- coding: utf-8 -*-
# @Author: ruian2, kelu2
# @Date:   2017-04-01 21:34:40
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-23 22:29:37
# import bpy

import pymesh
import numpy as np

redVal = 252
greenVal = 203
blueVal = 225

def gridGen(mesh_name):
    # print("entered gridGen")
    mesh = pymesh.load_mesh(mesh_name)
    mesh.enable_connectivity()
    grid = {}
    print mesh.vertices
    # print(len(mesh.vertices))
    for v in range(len(mesh.vertices)):
        grid[v] = list(mesh.get_vertex_adjacent_vertices(int(v)))
    # print grid
    return grid


def alpha_blending(src, dest, alpha):
    list = alpha * (src - dest) + dest
    result = []
    for i in list:
        result.append(int(i))
    return result


def color_vertices(obj, alpha, mesh_name):
    mesh = obj
    mesh.add_attribute("vertex_color")
    vertices_colors = np.zeros(3 * mesh.num_vertices)
    for i in range(mesh.num_vertices):
        vertices_colors[0 + 3 * i] = redVal
        vertices_colors[1 + 3 * i] = greenVal
        vertices_colors[2 + 3 * i] = blueVal
    for i in range(mesh.num_vertices):
        vertices_colors[i*3: i*3+3] = alpha_blending(vertices_colors[i*3: i*3+3], np.array([251, 247, 240]), alpha[i])
        # vertices_colors[i*3: i*3+3] = alpha_blending(vertices_colors[i*3: i*3+3], np.array([255,255,255]), alpha[i])

    mesh.set_attribute("vertex_color", vertices_colors)

    pymesh.save_mesh(mesh_name[:-4]+".ply", mesh, "vertex_color", ascii=True)


def change_format(inputFileName, outputFileName):
    file = open(inputFileName)
    lines = []
    for line in file:
        lines.append(line)
    # print lines
    file.close()
    num_vertices = int(lines[3][15:-1])
    del lines[7]
    lines.insert(7, "property uchar red\n")
    lines.insert(8, "property uchar green\n")
    lines.insert(9, "property uchar blue\n")
    for i in range(13,num_vertices+13):
        line_list = lines[i].split(" ")
        del line_list[3]
        new_line = " ".join(line_list)
        del lines[i]
        lines.insert(i, new_line)
    # print lines[13:13+num_vertices]
    # print num_vertices
    # print lines
    file = open(outputFileName, "w")
    for line in lines:
        file.write(line)
    file.close()


def get_mesh(mesh_name):
    mesh = pymesh.load_mesh(mesh_name)
    mesh.enable_connectivity()
    return mesh

