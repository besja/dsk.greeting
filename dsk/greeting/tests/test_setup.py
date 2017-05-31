# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from dsk.greeting.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of dsk.greeting into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if dsk.greeting is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('dsk.greeting'))

    def test_uninstall(self):
        """Test if dsk.greeting is cleanly uninstalled."""
        self.installer.uninstallProducts(['dsk.greeting'])
        self.assertFalse(self.installer.isProductInstalled('dsk.greeting'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IDskGreetingLayer is registered."""
        from dsk.greeting.interfaces import IDskGreetingLayer
        from plone.browserlayer import utils
        self.failUnless(IDskGreetingLayer in utils.registered_layers())
