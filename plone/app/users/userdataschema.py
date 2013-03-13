from zope.interface import Interface, implements
from zope import schema
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations

from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.CMFDefault.formlib.schema import FileUpload
from Products.CMFPlone import PloneMessageFactory as _

SCHEMA_ANNOTATION = "plone.app.users.schema"


class IUserDataSchemaProvider(Interface):
    """
    """

    def getSchema():
        """
        """


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        schema = IUserDataZ3CSchema
        # import in time to avoid circular imports errors
        from .schemaeditor import get_ttw_edited_schema
        ttwschema = get_ttw_edited_schema()
        for name in ttwschema:
            schema._InterfaceClass__attrs[name] = ttwschema[name]
        return schema


def checkEmailAddress(value):
    """Check for the user email address"""
    portal = getUtility(ISiteRoot)

    reg_tool = getToolByName(portal, 'portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True


class IUserDataBaseSchema(Interface):
    """
    """

    fullname = schema.TextLine(
        title=_(u'label_full_name', default=u'Full Name'),
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=False)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)

    home_page = schema.TextLine(
        title=_(u'label_homepage', default=u'Home page'),
        description=_(u'help_homepage',
                      default=u"The URL for your external home page, "
                      "if you have one."),
        required=False)

    description = schema.Text(
        title=_(u'label_biography', default=u'Biography'),
        description=_(u'help_biography',
                      default=u"A short overview of who you are and what you "
                      "do. Will be displayed on your author page, linked "
                      "from the items you create."),
        required=False)

    location = schema.TextLine(
        title=_(u'label_location', default=u'Location'),
        description=_(u'help_location',
                      default=u"Your location - either city and "
                      "country - or in a company setting, where "
                      "your office is located."),
        required=False)


class IUserDataSchema(IUserDataBaseSchema):

    portrait = FileUpload(title=_(u'label_portrait', default=u'Portrait'),
        description=_(u'help_portrait',
                      default=u'To add or change the portrait: click the '
                      '"Browse" button; select a picture of yourself. '
                      'Recommended image size is 75 pixels wide by 100 '
                      'pixels tall.'),
        required=False)

    pdelete = schema.Bool(
        title=_(u'label_delete_portrait', default=u'Delete Portrait'),
        description=u'',
        required=False)


class IUserDataZ3CSchema(IUserDataBaseSchema):
    """Overrides to make the schema z3c-compliant"""

    portrait = NamedBlobImage(title=_(u'label_portrait', default=u'Portrait'),
        description=_(u'help_portrait',
                      default=u'To add or change the portrait: click the '
                      '"Browse" button; select a picture of yourself. '
                      'Recommended image size is 75 pixels wide by 100 '
                      'pixels tall.'),
        required=False)
    form.widget(portrait='plone.app.users.browser.z3cpersonalpreferences.NamedImageFieldWidget')
