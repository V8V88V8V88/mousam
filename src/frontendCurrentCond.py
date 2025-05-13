import gi
from gi.repository import Gtk
from .constants import icons, conditon
from .config import settings
from gettext import gettext as _, pgettext as C_

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


class CurrentCondition(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_hexpand(True)
        # self.set_halign(Gtk.Align.FILL)
        # self.set_css_classes(['cond_grid'])
        self.paint_ui()

    def paint_ui(self):
        from .weatherData import current_weather_data as data

        # ========== left section ===========
        box_left = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            halign=Gtk.Align.START,
            margin_top=30,
        )
        self.attach(box_left, 0, 0, 1, 1)

        condition_grid = Gtk.Grid()
        box_left.append(condition_grid)

        # condition icon
        weather_code = data.weathercode.get("data")
        condition_icon = icons[str(weather_code)]
        if data.is_day.get("data") == 0:
            condition_icon = icons[str(weather_code) + "n"]

        icon_main = Gtk.Image().new_from_file(condition_icon)
        icon_main.set_hexpand(True)
        icon_main.set_pixel_size(64)
        condition_grid.attach(icon_main, 0, 0, 1, 2)

        # Condition label
        cond_label = Gtk.Label(
            label=conditon[str(data.weathercode.get("data"))],
            halign=Gtk.Align.START,
            valign=Gtk.Align.END,
        )
        cond_label.set_css_classes(["text-2b", "light-4", "bold-2"])
        condition_grid.attach(cond_label, 1, 0, 1, 1)

        # Condition temperature
        main_temp_label = Gtk.Label(
            label="{0:.0f} {1}".format(
                data.temperature_2m.get("data"), data.temperature_2m.get("unit")
            ),
            halign=Gtk.Align.START,
            valign=Gtk.Align.START,
        )
        main_temp_label.set_css_classes(["main_temp_label", "bold-1"])
        condition_grid.attach(main_temp_label, 1, 1, 1, 1)

        # ========== right  section ==========
        box_right = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, margin_top=35, margin_end=5
        )
        self.attach(box_right, 1, 0, 1, 1)

        self.selected_city_index = list(
            map(lambda city: settings.selected_city in city, settings.added_cities)
        ).index(True)

        city_arr = settings.added_cities[self.selected_city_index].split(",")

        # Delete lat,lon from the array
        del city_arr[-1]
        del city_arr[-1]

        box_label = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_bottom=10)
        box_right.append(box_label)

        loc_label_city = Gtk.Label(
            label=city_arr[0], halign=Gtk.Align.END, margin_bottom=1
        )
        loc_label_city.set_css_classes(["text-2b", "bold-2"])
        box_label.append(loc_label_city)

        loc_label_country = Gtk.Label(
            label=city_arr[1], valign=Gtk.Align.END, halign=Gtk.Align.END
        )
        loc_label_country.set_css_classes(["text-4", "light-3"])
        box_label.append(loc_label_country)

        feels_like_label = Gtk.Label(halign=Gtk.Align.END, margin_bottom=5)
        markup_text = _("Feels like • <b> {0} {1}</b>").format(
            data.apparent_temperature.get("data"), data.apparent_temperature.get("unit")
        )
        feels_like_label.set_markup(markup_text)
        feels_like_label.set_css_classes(["text-5", "bold-3d"])
        box_right.append(feels_like_label)

        # visibility_label = Gtk.Label(halign=Gtk.Align.END, margin_bottom=5)
        # markup_text = "Visibility • <b> {0:.1f} {1}</b>".format(
        #     data.visibility.get("data"), data.visibility.get("unit")
        # )
        # visibility_label.set_markup(markup_text)
        # visibility_label.set_css_classes(["text-4", "bold-3"])
        # box_right.append(visibility_label)
