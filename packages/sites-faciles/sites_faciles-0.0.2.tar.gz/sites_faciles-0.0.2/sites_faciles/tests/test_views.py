from django.contrib.auth.models import User
from django.core.management import call_command
from wagtail.models import Page, Site
from wagtail.rich_text import RichText
from wagtail.test.utils import WagtailPageTestCase
from wagtailmenus.models.menuitems import FlatMenuItem, MainMenuItem
from wagtailmenus.models.menus import FlatMenu, MainMenu

from wagtail_design_system.models import ContentPage, MegaMenu, MegaMenuCategory, SitesFacilesConfig


class ContentPageTestCase(WagtailPageTestCase):
    def setUp(self):
        home = Page.objects.get(slug="home")
        self.admin = User.objects.create_superuser("test", "test@test.test", "pass")
        self.admin.save()
        self.content_page = home.add_child(
            instance=ContentPage(
                title="Page de contenu",
                slug="content-page",
                owner=self.admin,
            )
        )
        self.content_page.save()

    def test_content_page_is_renderable(self):
        self.assertPageIsRenderable(self.content_page)

    def test_content_page_has_minimal_content(self):
        url = self.content_page.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "<title>Page de contenu — Titre du site</title>",
        )


class ConfigTestCase(WagtailPageTestCase):
    def setUp(self):
        home = Page.objects.get(slug="home")
        self.admin = User.objects.create_superuser("test", "test@test.test", "pass")
        self.admin.save()
        self.content_page = home.add_child(
            instance=ContentPage(
                title="Page de contenu",
                slug="content-page",
                owner=self.admin,
            )
        )
        self.content_page.save()

        self.config, _created = SitesFacilesConfig.objects.update_or_create(
            site_id=1,
            defaults={
                "site_title": "Site title",
                "site_tagline": "Site tagline",
                "header_brand": "République française",
                "header_brand_html": "République<br />française",
                "footer_brand": "République française",
                "footer_brand_html": "République<br />française",
                "footer_description": "Site <b>description</b>.",
            },
        )
        self.config.save()

    def test_header_brand_block_uses_conf(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertInHTML(
            """<a href="/"
                title="Accueil — République française">
                <p class="design-system-logo">République<br />française</p>
            </a>""",
            response.content.decode(),
        )

    def test_footer_brand_block_uses_conf(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertInHTML(
            """<div class="design-system-footer__brand design-system-enlarge-link">
                <a id="footer-operator" href="/"
                    title="Retour à l’accueil du site - Site title - République française">
                    <p class="design-system-logo">
                        République<br />française
                    </p>
                </a>
            </div>""",
            response.content.decode(),
        )

    def test_header_title_block_uses_conf(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertInHTML(
            """<div class="design-system-header__service">
                <a href="/" title="Accueil — Site title">
                    <p class="design-system-header__service-title">Site title</p>
                </a>
                <p class="design-system-header__service-tagline">Site tagline</p>
            </div>""",
            response.content.decode(),
        )

    def test_notice_is_not_set_by_default(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertNotContains(
            response,
            "design-system-notice__body",
        )

    def test_notice_can_be_set(self):
        self.config.notice = "Ceci est une information <b>importante</b> et <i>temporaire</i>."
        self.config.save()

        url = self.content_page.url
        response = self.client.get(url)

        self.assertInHTML(
            """<div class="design-system-notice design-system-notice--info">
                <div class="design-system-container">
                    <div class="design-system-notice__body">
                        <p class="design-system-notice__title">
                            Ceci est une information <b>importante</b> et <i>temporaire</i>.
                        </p>
                    </div>
                </div>
            </div>""",
            response.content.decode(),
        )

    def test_beta_tag_is_not_set_by_default(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertNotContains(
            response,
            '<span class="design-system-badge design-system-badge--sm design-system-badge--green-emeraude">BETA</span>',
        )

    def test_beta_tag_can_be_set(self):
        self.config.beta_tag = True
        self.config.save()

        url = self.content_page.url
        response = self.client.get(url)

        self.assertContains(
            response,
            '<span class="design-system-badge design-system-badge--sm design-system-badge--green-emeraude">BETA</span>',
        )

    def test_footer_description_uses_conf(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertInHTML(
            """<p class="design-system-footer__content-desc">
                    Site <b>description</b>.
                </p>""",
            response.content.decode(),
        )


class MenusTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        call_command("create_starter_pages")

    def setUp(self) -> None:
        self.site = Site.objects.filter(is_default_site=True).first()
        self.home_page = self.site.root_page

        self.main_menu = MainMenu.objects.create(site=self.site)

        MainMenuItem.objects.create(link_page=self.home_page, menu=self.main_menu, link_text="Accueil", sort_order=0)

        body = []

        text_raw = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>"""
        body.append(("paragraph", RichText(text_raw)))

        self.publications_page = self.home_page.add_child(
            instance=ContentPage(title="Publications", body=body, show_in_menus=True)
        )

        self.example_publication_page = self.publications_page.add_child(
            instance=ContentPage(title="Publication 1", body=body, show_in_menus=True)
        )
        self.publications_menu_item = MainMenuItem.objects.create(
            link_page=self.publications_page, menu=self.main_menu, sort_order=2
        )

    def test_basic_menu_is_rendered(self):
        self.assertPageIsRenderable(self.home_page)
        response = self.client.get(self.home_page.url)

        # Selected menu item : home page
        self.assertInHTML(
            '<a class="design-system-nav__link" href="/" aria-current="page" target="_self">Accueil</a>',
            response.content.decode(),
        )

        self.assertInHTML(
            f"""<button class="design-system-nav__btn"
                aria-expanded="false"
                aria-controls="menu-{self.publications_menu_item.link_page.pk}">
                Publications
            </button>""",
            response.content.decode(),
        )

        self.assertInHTML(
            '<a class="design-system-nav__link" href="/publications/publication-1/" target="_self">Publication 1</a>',
            response.content.decode(),
        )

        # Selected menu item : publication 1
        response = self.client.get(self.example_publication_page.url)
        self.assertInHTML(
            '<a class="design-system-nav__link" href="/" target="_self">Accueil</a>',
            response.content.decode(),
        )

        self.assertInHTML(
            f"""<button class="design-system-nav__btn"
                aria-current="true"
                aria-expanded="false"
                aria-controls="menu-{self.publications_menu_item.link_page.pk}">
                    Publications
            </button>""",
            response.content.decode(),
        )

        self.assertInHTML(
            """<a class="design-system-nav__link"
                aria-current="page"
                href="/publications/publication-1/"
                target="_self">
                Publication 1
            </a>""",
            response.content.decode(),
        )

    def test_mega_menu_is_rendered(self):
        publications_mega_menu = MegaMenu.objects.create(
            name="Méga-menu publications",
            parent_menu_item=self.publications_menu_item,
            description="Ceci est une description",
        )

        menu_category_menu = FlatMenu.objects.create(
            site_id=self.site.id,
            title="Menu publications > Catégorie 1",
            handle="mega_menu_section_1",
            heading="Colonne 1",
        )

        MegaMenuCategory.objects.create(mega_menu=publications_mega_menu, sort_order=0, category=menu_category_menu)

        FlatMenuItem.objects.get_or_create(
            link_page=self.example_publication_page, menu=menu_category_menu, sort_order=0
        )

        self.assertPageIsRenderable(self.example_publication_page)
        response = self.client.get(self.example_publication_page.url)

        self.assertInHTML(
            '<p class="design-system-hidden design-system-displayed-lg">Ceci est une description</p>',
            response.content.decode(),
        )

        self.assertInHTML(
            f"""<button class="design-system-nav__btn"
                        aria-expanded="false"
                        aria-current="true"
                        aria-controls="mega-menu-{self.publications_menu_item.id}">Publications</button>
            """,
            response.content.decode(),
        )

        self.assertInHTML(
            """<a class="design-system-nav__link"
                aria-current="page"
                href="/publications/publication-1/"
                target="_self">
                    Publication 1
                </a>""",
            response.content.decode(),
        )


# sites_faciles_dashboard


class DashboardTestCase(WagtailPageTestCase):
    def setUp(self):
        home = Page.objects.get(slug="home")
        self.admin = User.objects.create_superuser("test", "test@test.test", "pass")
        self.admin.save()

        self.content_page = home.add_child(
            instance=ContentPage(
                title="Page de contenu",
                slug="content-page",
                owner=self.admin,
            )
        )
        self.content_page.save()

    def test_userbar_is_present_when_logged_in(self):
        url = self.content_page.url
        response = self.client.get(url)
        self.assertNotContains(
            response,
            '<svg class="icon icon-edit w-userbar-icon" aria-hidden="true"><use href="#icon-edit"></use></svg>',
            html=True,
        )

        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertContains(
            response,
            '<svg class="icon icon-edit w-userbar-icon" aria-hidden="true"><use href="#icon-edit"></use></svg>',
            html=True,
        )
