from whyis.plugin import Plugin, NanopublicationListener
from whyis.namespace import NS
from flask_pluginengine import PluginBlueprint, current_plugin
from flask import current_app, render_template
import rdflib
import json
import collections
from functools import reduce


whyis = NS.whyis

plugin_blueprint = PluginBlueprint('fediverse', __name__)

class FediversePlugin(Plugin):

    def create_blueprint(self):
        return plugin_blueprint

    def init(self):
        NS.astr = rdflib.Namespace("https://www.w3.org/ns/activitystreams#")
