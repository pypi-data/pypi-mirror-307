#!/usr/bin/env python3
"""
Command line utility that loads Brick files and loads them into an AGX Simulation
"""
from rebrick.brickapplication import BrickApplication

def brickview_build_scene():
    BrickApplication.prepareScene()

def run():
    BrickApplication(brickview_build_scene).run()

if __name__ == "__main__":
    run()
