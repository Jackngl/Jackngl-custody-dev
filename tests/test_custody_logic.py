
import unittest
from datetime import datetime, date, time, timedelta
from unittest.mock import MagicMock
from custom_components.custody_schedule.schedule import CustodyScheduleManager, CustodyWindow
from custom_components.custody_schedule.const import (
    CONF_ARRIVAL_TIME,
    CONF_DEPARTURE_TIME,
    CONF_END_DAY,
    CONF_COUNTRY,
    CONF_ZONE,
)

class MockHolidays:
    async def async_list(self, country, zone):
        return []

class TestCustodyLogic(unittest.TestCase):
    def setUp(self):
        self.hass = MagicMock()
        self.hass.config.time_zone = "UTC"
        self.holidays = MockHolidays()
        
    def test_calculate_end_date_sunday_default(self):
        config = {
            CONF_ARRIVAL_TIME: "08:00",
            CONF_DEPARTURE_TIME: "19:00",
            CONF_END_DAY: "sunday"
        }
        manager = CustodyScheduleManager(self.hass, config, self.holidays)
        
        # Friday Oct 3, 2025
        start_date = datetime(2025, 10, 3, 8, 0) 
        holidays = set()
        
        end_date = manager._calculate_end_date(start_date, holidays)
        
        # Should be Sunday Oct 5, 2025
        self.assertEqual(end_date.date(), date(2025, 10, 5))
        self.assertEqual(end_date.weekday(), 6) # Sunday

    def test_calculate_end_date_monday_return(self):
        config = {
            CONF_ARRIVAL_TIME: "08:00",
            CONF_DEPARTURE_TIME: "19:00",
            CONF_END_DAY: "monday"
        }
        manager = CustodyScheduleManager(self.hass, config, self.holidays)
        
        # Friday Oct 3, 2025
        start_date = datetime(2025, 10, 3, 8, 0)
        holidays = set()
        
        end_date = manager._calculate_end_date(start_date, holidays)
        
        # Should be Monday Oct 6, 2025
        self.assertEqual(end_date.date(), date(2025, 10, 6))
        self.assertEqual(end_date.weekday(), 0) # Monday

    def test_calculate_end_date_holiday_extension(self):
        config = {
            CONF_ARRIVAL_TIME: "08:00",
            CONF_DEPARTURE_TIME: "19:00",
            CONF_END_DAY: "monday"
        }
        manager = CustodyScheduleManager(self.hass, config, self.holidays)
        
        # Friday Oct 3, 2025
        start_date = datetime(2025, 10, 3, 8, 0)
        # Monday Oct 6 is a holiday
        holidays = {date(2025, 10, 6)}
        
        end_date = manager._calculate_end_date(start_date, holidays)
        
        # Should be Tuesday Oct 7, 2025
        self.assertEqual(end_date.date(), date(2025, 10, 7))
        self.assertEqual(end_date.weekday(), 1) # Tuesday

    def test_calculate_end_date_long_holiday_extension(self):
        config = {
            CONF_ARRIVAL_TIME: "08:00",
            CONF_DEPARTURE_TIME: "19:00",
            CONF_END_DAY: "monday"
        }
        manager = CustodyScheduleManager(self.hass, config, self.holidays)
        
        # Friday Oct 3, 2025
        start_date = datetime(2025, 10, 3, 8, 0)
        # Monday Oct 6 and Tuesday Oct 7 are holidays
        holidays = {date(2025, 10, 6), date(2025, 10, 7)}
        
        end_date = manager._calculate_end_date(start_date, holidays)
        
        # Should be Wednesday Oct 8, 2025
        self.assertEqual(end_date.date(), date(2025, 10, 8))
        self.assertEqual(end_date.weekday(), 2) # Wednesday

    def test_alternate_week_monday_to_monday(self):
        config = {
            CONF_ARRIVAL_TIME: "08:00",
            CONF_DEPARTURE_TIME: "19:00",
            CONF_END_DAY: "monday"
        }
        manager = CustodyScheduleManager(self.hass, config, self.holidays)
        
        # Monday Oct 6, 2025
        start_date = datetime(2025, 10, 6, 8, 0)
        holidays = set()
        
        end_date = manager._calculate_end_date(start_date, holidays)
        
        # Should be Monday Oct 13, 2025 (7 days later)
        self.assertEqual(end_date.date(), date(2025, 10, 13))
        self.assertEqual((end_date - start_date).days, 7)

if __name__ == "__main__":
    unittest.main()
