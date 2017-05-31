# -*- coding: utf-8 -*-

from plone.directives import form

from zope import schema
import z3c.form
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Zope3PageTemplateFile

from plone.autoform import directives


from dsk.greeting import MessageFactory as _


from dsk.greeting.utils import validateaddress, trusted

from zope.interface import invariant, Invalid
from zope.component import getUtility, getMultiAdapter
from smtplib import SMTPException, SMTPRecipientsRefused
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IMailSchema


from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

from plone.app.uuid.utils import uuidToObject

#def getCards(context):
#    path = context.getPhysicalPath()
#    path = "/".join(path)
#    brains = context.portal_catalog(path={"query": path, "depth": 1, "portal_type": "Image"})
#    terms = [] 
#    for i in brains:
#        row = SimpleTerm(value = i.UID, title = i.getObject().absolute_url())
#        terms.append(row)
#    return SimpleVocabulary(terms)

# directlyProvides(getCards, IContextSourceBinder)



class IGreetingForm(form.Schema):
    """ Define form fields """

    recipient = schema.TextLine(
            title=_(u"Name of receptor"),
            required=True
        )
    location = schema.TextLine(
            title=_(u"Station and room number"),
            required=True 
        )
    name = schema.TextLine(
            title=_(u"Your name"),
            required=True 
        )
    email = schema.TextLine(
            title=_(u"Your email"),
            required=True, 
            constraint=validateaddress
        )
    message = schema.Text(
            title=_(u"Your greeting"),
            required=True 
        )
    image = schema.TextLine(
            title=_(u"Image"),
            required=True
        )

    directives.mode(image='hidden')
 

class GreetingForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@greeting-form

    """
    template = Zope3PageTemplateFile("form.pt")
    schema = IGreetingForm
    ignoreContext = True


    def _redirect(self, target=''):
        if not target:
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            target = portal_state.portal_url()
        self.request.response.redirect(target)

    def WidgetsDict(self):
        widgets_dict = {}
        for widget in self.widgets.values():
            widgets_dict[widget.id] = widget
        return widgets_dict

    @z3c.form.button.buttonAndHandler(_(u'Send'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        portal = getToolByName(self, 'portal_url').getPortalObject()
        encoding = portal.getProperty('email_charset', 'utf-8')

        data['image_object'] = uuidToObject(data['image'])
         
        trusted_template = trusted(portal.greeting_email)

        mail_text = trusted_template(self, charset=encoding, data = data)

        subject = self.context.translate(_(u"New greeting"))

        if isinstance(mail_text, unicode):
            mail_text = mail_text.encode(encoding)

        host = getToolByName(self, 'MailHost')

        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        m_to = mail_settings.email_from_address

        m_from = m_to

        print m_to

        try:
            host.send(mail_text, m_to, m_from, subject=subject,
                      charset=encoding, immediate=True, msg_type="text/html")

            print m_to

        except SMTPRecipientsRefused:

            raise SMTPRecipientsRefused(
                _(u'Recipient address rejected by server.'))

        except SMTPException as e:
            raise(e)
        
        IStatusMessage(self.request).add(_(u"Submit complete"), type='info')
        return self._redirect(target=self.context.absolute_url())


    @z3c.form.button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """