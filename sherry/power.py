"""
Drivers for OBM power on/off handling
"""

import logging
import subprocess


LOG = logging.getLogger(__name__)


class PowerDriver(object):
    """Abstraction for powering on/off nodes"""

    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password

    def power_on(self):
        """Power the node on"""
        raise NotImplementedError()

    def power_off(self):
        """Power the node off"""
        raise NotImplementedError()

    def reboot(self):
        """Reboot the node"""
        self.power_off()
        self.power_on()


class MockPowerDriver(PowerDriver):
    """A power driver that does nothing but log the requests"""

    def power_on(self):
        LOG.debug('Powering on at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))

    def power_off(self):
        LOG.debug('Powering off at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))

    def reboot(self):
        LOG.debug('Rebooting at {0}@{1}, passwd: %{2}'
                  .format(self.user, self.address, self.password))


class IPMIDriver(PowerDriver):
    """Power on/off using ipmitool"""

    def _call_ipmitool(self, action):
        """Helper to call ipmitool"""
        subprocess.call(['/usr/bin/ipmitool',
                         '-H', str(self.address),
                         '-U', str(self.user),
                         '-P', str(self.password),
                         'power', str(action)])

    def power_on(self):
        self._call_ipmitool('on')

    def power_off(self):
        self._call_ipmitool('off')

    def reboot(self):
        self._call_ipmitool('cycle')


class QemuDriver(PowerDriver):
    """Power on/off Qemu/KVM virtual machines using virsh"""

    def _call_virsh(self, action):
        """Helper to call virsh"""
        # XXX: requires libvirt to be configured for password-less operation
        subprocess.call(['/usr/bin/virsh'
                         '--connect',
                         'qemu://127.0.0.1@{1}/system'.format(self.user),
                         str(action),
                         str(self.address)])

    def power_on(self):
        self._call_virsh('on')

    def power_off(self):
        self._call_virsh('off')
