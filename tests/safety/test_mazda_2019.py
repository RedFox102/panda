#!/usr/bin/env python3
import unittest
from panda import Panda
from panda.tests.libpanda import libpanda_py
import panda.tests.safety.common as common
from panda.tests.safety.common import CANPackerPanda


class TestMazda2019Safety(common.PandaSafetyTest, common.DriverTorqueSteeringSafetyTest):

  TX_MSGS = [[0x249, 1], [0x220, 2]]
  STANDSTILL_THRESHOLD = .1
  RELAY_MALFUNCTION_ADDR = 0x217
  RELAY_MALFUNCTION_BUS = 0
  FWD_BLACKLISTED_ADDRS = {0: [0x220]}
  FWD_BUS_LOOKUP = {0: 2, 2: 0}

  MAX_RATE_UP = 45
  MAX_RATE_DOWN = 80
  MAX_TORQUE = 8000

  MAX_RT_DELTA = 1688
  RT_INTERVAL = 250000

  DRIVER_TORQUE_ALLOWANCE = 1400
  DRIVER_TORQUE_FACTOR = 1

  def setUp(self):
    self.packer = CANPackerPanda("mazda_2019")
    self.safety = libpanda_py.libpanda
    self.safety.set_safety_hooks(Panda.SAFETY_MAZDA_2019, 0)
    self.safety.init_tests()

  
  def _torque_driver_msg(self, torque):
    values = {"STEER_TORQUE_SENSOR": torque}
    return self.packer.make_can_msg_panda("EPS_FEEDBACK", 0, values)

  def _torque_cmd_msg(self, torque, steer_req=1):
    values = {"LKAS_REQUEST": torque}
    return self.packer.make_can_msg_panda("EPS_LKAS", 1, values)

  def _speed_msg(self, speed):
    values = {"SPEED": speed}
    return self.packer.make_can_msg_panda("SPEED", 2, values)

  def _user_brake_msg(self, brake):
    values = {"BRAKE_PEDAL_PRESSED": brake}
    return self.packer.make_can_msg_panda("BRAKE_PEDAL", 0, values)

  def _user_gas_msg(self, gas):
    values = {"PEDAL_GAS": gas}
    return self.packer.make_can_msg_panda("ENGINE_DATA", 2, values)

  def _pcm_status_msg(self, enable):
    values = {"CRZ_ENABLED": enable,
              "PRE_ENABLE": enable}
    return self.packer.make_can_msg_panda("CRUZE_STATE", 0, values)

if __name__ == "__main__":
  unittest.main()
