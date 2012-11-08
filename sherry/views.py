"""
Flask views and routes for controlling pxe booting.
"""

import logging
import jinja2

from flask import render_template
from flask import request

from sherry import app

log = app.logger

# This stores the how to reimage the next client to request
reimage_info = None

# The list of images hosted at this app
images = [k.replace('_IMAGE_LOCATION', '').lower()
            for k in app.config.keys() if k.endswith('_IMAGE_LOCATION')]


@app.route('/')
def index():
    global reimage_info, images
    return render_template(
            'index.html', reimage_info=reimage_info, images=images)


@app.route('/pxe/chain.pxe', methods=['GET'])
def boot_or_install():
    global reimage_info
    if reimage_info is None:
        log.info('Served {} boot.pxe'.format(request.remote_addr))
        return render_template('boot.pxe')
    result = render_template('install.pxe', **reimage_info)
    log.info('Served {} install.pxe with info {!s}'.format(
            request.remote_addr, reimage_info))
    reimage_info = None
    return result


# allows both HTTP methods for convenience. Bookmark reimage ftw!
@app.route('/reimage/<image_type>', methods=['GET', 'POST'])
def reimage(image_type):
    """ Initiate a reimage of the target system.  """
    global reimage_info, images
    image_type = image_type.upper()
    location = app.config.get('{}_IMAGE_LOCATION'.format(image_type))
    kernel_opts = app.config.get('{}_KERNEL_OPTS'.format(image_type), '')
    if location is None:
        message = ('Could not reimage. Unknown image type {}.'.format(image_type))
        log.warning(message)
        return render_template('reimage.html', message=message, images=images)

    # store the parameters for the next boot request
    reimage_info = dict(location=location, kernel_opts=kernel_opts)

    log.info('Rebooting {}.'.format(request.remote_addr))
    powerdriver = app.config['POWER_DRIVER']()
    power_results = powerdriver.reboot()

    message = "Reimaging {}. Power command results: {}".format(
            request.remote_addr, power_results)
    log.info(message)
    return render_template('reimage.html', message=message, images=images)


@app.route('/log')
def display_log():
    """ Display recent lines of log messages """
    messages = [r.getMessage() for r in app.memory_log.records]
    return render_template('log.html', log=messages, images=images)
