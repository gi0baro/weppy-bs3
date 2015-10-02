# -*- coding: utf-8 -*-
"""
    weppy_bs3.ext
    -------------

    Provides the bootstrap3 extension for weppy

    :copyright: (c) 2015 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

import os
import shutil
from weppy import tag, asis
from weppy.extensions import Extension, TemplateExtension, TemplateLexer
from weppy.forms import FormStyle


class BS3(Extension):
    default_static_folder = 'bs3'
    default_config = dict(
        set_as_default_style=True,
        static_folder='bs3',
        date_format="DD/MM/YYYY",
        time_format="HH:mm:ss",
        datetime_format="DD/MM/YYYY HH:mm:ss",
        time_pickseconds=True,
        icon_time='fa fa-clock-o',
        icon_date='fa fa-calendar',
        icon_up='fa fa-arrow-up',
        icon_down='fa fa-arrow-down'
    )
    assets = [
        'bootstrap.min.js',
        'bootstrap.min.css',
        'moment.min.js',
        'bootstrap-datetimepicker.min.js',
        'bootstrap-datetimepicker.min.css']

    def _load_config(self):
        for key, value in self.default_config.items():
            self.config[key] = self.config.get(key, value)
        self.env.folder = os.path.join(self.app.static_path,
                                       self.config.static_folder)

    def on_load(self):
        # init and create required folder
        self._load_config()
        if not os.path.exists(self.env.folder):
            os.mkdir(self.env.folder)
        # load assets and copy to app
        for asset in self.assets:
            static_file = os.path.join(self.env.folder, asset)
            if not os.path.exists(static_file):
                source_file = os.path.join(
                    os.path.dirname(__file__), 'assets', asset)
                shutil.copy2(source_file, static_file)
        # set formstyle if needed
        if self.config.set_as_default_style:
            self.app.config.ui.forms_style = BS3FormStyle
        # init template extension
        self.env.assets = self.assets
        self.app.add_template_extension(BS3Template)

    @property
    def FormStyle(self):
        return BS3FormStyle


class BS3Lexer(TemplateLexer):
    evaluate_value = False

    def process(self, value):
        for asset in self.ext.env.assets:
            file_ext = asset.rsplit(".", 1)[-1]
            url = "/static/"+self.ext.config.static_folder+"/"+asset
            if file_ext == "js":
                static = '<script type="text/javascript" src="'+url+'"></script>'
            else:
                static = '<link rel="stylesheet" href="'+url+'" type="text/css">'
            node = self.parser.create_htmlnode(static, pre_extend=False)
            self.top.append(node)
        ## add font awesome from external cdn
        url = '//maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
        static = '<link href="'+url+'" rel="stylesheet">'
        node = self.parser.create_htmlnode(static, pre_extend=False)
        self.top.append(node)


class BS3Template(TemplateExtension):
    namespace = 'BS3'
    lexers = {'include_bs3': BS3Lexer}


_datepicker_xml = """
<script type="text/javascript">
    $(function() {
        $('#%(divid)s').datetimepicker({
            pickTime: false,
            format: '%(format)s',
            minDate: %(minDate)s,
            maxDate: %(maxDate)s,
            icons: {
                date: "%(icon_date)s",
                up: "%(icon_up)s",
                down: "%(icon_down)s"
            }
        });
    });
</script>"""

_timepicker_xml = """
<script type="text/javascript">
    $(function() {
        $('#%(divid)s').datetimepicker({
            pickDate: false,
            useSeconds: %(use_seconds)s,
            format: '%(format)s',
            icons: {
                time: "%(icon_time)s",
                up: "%(icon_up)s",
                down: "%(icon_down)s"
            }
        });
    });
</script>"""

_datetimepicker_xml = """
<script type="text/javascript">
    $(function() {
        $('#%(divid)s').datetimepicker({
            useSeconds: %(use_seconds)s,
            format: '%(format)s',
            minDate: %(minDate)s,
            maxDate: %(maxDate)s,
            icons: {
                date: "%(icon_date)s",
                time: "%(icon_time)s",
                up: "%(icon_up)s",
                down: "%(icon_down)s"
            }
        });
    });
</script>"""


class BS3FormStyle(FormStyle):
    @staticmethod
    def widget_bool(attr, field, value, _id=None):
        return FormStyle.widget_bool(attr, field, value,
                                     _class="bool checkbox", _id=_id)

    @staticmethod
    def widget_date(attr, field, value, _class='date', _id=None):
        def load_js():
            dformat = attr.get('date_format', attr['env'].date_format)
            icon_up = attr.get('icon_up', attr['env'].icon_up)
            icon_down = attr.get('icon_down', attr['env'].icon_down)
            s = asis(_datepicker_xml % dict(
                     divid=fid+"_cat",
                     format=dformat,
                     minDate=dates["minDate"],
                     maxDate=dates["maxDate"],
                     icon_date=icon_date,
                     icon_up=icon_up,
                     icon_down=icon_down))
            return s

        icon_date = attr.get('icon_date', attr['env'].icon_date)
        dates = {}
        for dname in ["minDate", "maxDate"]:
            if not attr.get(dname):
                dates[dname] = '$.fn.datetimepicker.defaults.'+dname
            else:
                dates[dname] = '"'+attr[dname]+'"'
        fid = _id or field.name
        res = []
        js = load_js()
        res.append(
            tag.input(
                _name=field.name, _type='text', _id=fid, _class="form-control",
                value=str(value) if value is not None else '')
            )
        res.append(tag.span(tag.span(_class=icon_date),
                   _class="input-group-addon"))
        res.append(js)
        return tag.div(*res, _id=fid+"_cat", _class='input-group date')

    @staticmethod
    def widget_time(attr, field, value, _class='time', _id=None):
        def load_js():
            tformat = attr.get('time_format', attr['env'].time_format)
            icon_up = attr.get('icon_up', attr['env'].icon_up)
            icon_down = attr.get('icon_down', attr['env'].icon_down)
            pick_seconds = "true" if use_seconds else "false"
            s = asis(_timepicker_xml % dict(
                     divid=fid+"_cat",
                     format=tformat,
                     use_seconds=pick_seconds,
                     icon_time=icon_time,
                     icon_up=icon_up,
                     icon_down=icon_down))
            return s

        icon_time = attr.get('icon_time', attr['env'].icon_time)
        use_seconds = attr.get('time_pickseconds',
                               attr['env'].time_pickseconds)
        fid = _id or field.name
        res = []
        js = load_js()
        _value = str(value) if value is not None else ''
        if not use_seconds:
            _value = _value[:-2]
        res.append(
            tag.input(
                _name=field.name, _type='text', _id=fid, _class="form-control",
                value=_value)
            )
        res.append(tag.span(tag.span(_class=icon_time),
                   _class="input-group-addon"))
        res.append(js)
        return tag.div(*res, _id=fid+"_cat", _class='input-group time')

    @staticmethod
    def widget_datetime(attr, field, value, _class='datetime', _id=None):
        def load_js():
            dformat = attr.get('datetime_format', attr['env'].datetime_format)
            icon_time = attr.get('icon_time', attr['env'].icon_time)
            icon_up = attr.get('icon_up', attr['env'].icon_up)
            icon_down = attr.get('icon_down', attr['env'].icon_down)
            pick_seconds = "true" if use_seconds else "false"
            s = asis(_datetimepicker_xml % dict(
                     divid=fid+"_cat",
                     format=dformat,
                     use_seconds=pick_seconds,
                     minDate=dates["minDate"],
                     maxDate=dates["maxDate"],
                     icon_date=icon_date,
                     icon_time=icon_time,
                     icon_up=icon_up,
                     icon_down=icon_down))
            return s

        icon_date = attr.get('icon_date', attr['env'].icon_date)
        dates = {}
        for dname in ["minDate", "maxDate"]:
            if not attr.get(dname):
                dates[dname] = '$.fn.datetimepicker.defaults.'+dname
            else:
                dates[dname] = '"'+attr[dname]+'"'
        use_seconds = attr.get('time_pickseconds',
                               attr['env'].time_pickseconds)
        fid = _id or field.name
        res = []
        js = load_js()
        _value = str(value) if value is not None else ''
        if not use_seconds:
            _value = _value[:-2]
        res.append(
            tag.input(
                _name=field.name, _type='text', _id=fid, _class="form-control",
                value=_value)
            )
        res.append(tag.span(tag.span(_class=icon_date),
                   _class="input-group-addon"))
        res.append(js)
        return tag.div(*res, _id=fid+"_cat", _class='input-group datetime')

    def on_start(self):
        from weppy.expose import Expose
        self.attr['env'] = Expose.application.ext.BS3.config
        self.parent = tag.fieldset()

    def style_widget(self, widget):
        wtype = widget['_class'].split(' ')[0]
        if wtype not in ["bool", "upload_wrap", "input-group"]:
            widget['_class'] += " form-control"

    def create_label(self, label):
        wid = self.element.widget['_id']
        return tag.label(label, _for=wid, _class='col-sm-2 control-label')

    def create_comment(self, comment):
        return tag.p(comment, _class='help-block')

    def create_error(self, error):
        return tag.p(error, _class='text-danger')

    def add_widget(self, widget):
        _class = 'form-group'
        label = self.element.label
        wrapper = tag.div(widget, _class='col-sm-10')
        if self.element.error:
            wrapper.append(self.element.error)
            _class += ' has-error'
        if self.element.comment:
            wrapper.append(self.element.comment)
        self.parent.append(tag.div(label, wrapper, _class=_class))

    def add_buttons(self):
        submit = tag.input(_type='submit', _value=self.attr['submit'],
                           _class='btn btn-primary')
        buttons = tag.div(submit, _class="col-sm-10 col-sm-offset-2")
        self.parent.append(tag.div(buttons, _class='form-group'))

    def render(self):
        self.attr['_class'] = self.attr.get('_class', 'form-horizontal')
        return FormStyle.render(self)
