#!/usr/bin/env bash


function install_dependencies() {
    sudo apt-get update
    sudo apt-get update && sudo apt-get install -y portaudio19-dev
    sudo apt-get update && sudo apt-get install -y libgtk-3-dev libgstreamer1.0-dev libgtk2.0-dev libjpeg-dev libpng-dev libtiff-dev
}

install_dependencies
