import unittest
from platform import system

import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    def setUp(self) -> None:
        self.SR = SmartRoom()
        self.SR.light_on = False

     # first user story
    @patch.object(GPIO, 'input')
    def test_person_in(self, mock_input):
        mock_input.return_value = 0
        occupancy = self.SR.check_room_occupancy()
        self.assertTrue(occupancy)

    @patch.object(GPIO, 'input')
    def test_person_out(self, mock_input):
        mock_input.return_value = 5
        occupancy = self.SR.check_room_occupancy()
        self.assertFalse(occupancy)


    #second user story
    @patch.object(GPIO, 'input')
    def test_light_detection(self, mock_photoresistor) :
        mock_photoresistor.return_value = True
        system = SmartRoom()
        self.assertTrue(system.check_enough_light())

    @patch.object(GPIO, 'input')
    def test_light_not_detection(self, mock_photoresistor):
        mock_photoresistor.return_value = False
        system = SmartRoom()
        self.assertFalse(system.check_enough_light())

    #3rd user story
    @patch.object(GPIO, 'input')
    @patch.object(GPIO, 'output')
    def test_turn_bulb_on_yes_person_inside(self, mock_photoresistor, mock_red_light: Mock):
        mock_photoresistor.return_value = True
        system = SmartRoom()
        system.manage_light_level()
        mock_red_light.assert_called_once_with(system.LED_PIN, True)
        self.assertTrue(system.mock_red_light)

    @patch.object(GPIO, 'input')
    @patch.object(GPIO, 'output')
    def test_turn_bulb_off_no_person_inside(self, mock_photoresistor, mock_red_light: Mock):
        mock_photoresistor.return_value = False
        system = SmartRoom()
        system.manage_light_level()
        mock_red_light.assert_called_once_with(system.LED_PIN, False)
        self.assertTrue(system.mock_red_light)
















