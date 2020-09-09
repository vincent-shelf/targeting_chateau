
class BaseEngine:

    MIN_TIME_BEFORE_CALL = 2
    VERBOSITY = 1
    BASE_URL = ""

    def get_catalog_page_url(self, **kwargs):
        """
        Returns the URL of a catalog page based on engine-based arguments
        :param kwargs:
        :return:
        """
        pass

    def list_catalog_target_pages(self, proc):
        """
        Returns the list of catalog pages that need to be screened for ads
        :param proc:
        :return:
        """
        pass

    def extract_adlist_from_catalog_page(self, page_url, page):
        """
        Returns the list of ad page links to be processed from a catalog page
        :param page_url:
        :param page:
        :return:
        """
        pass

    def process_ad_page(self, ad_url, ad_page):
        """
        Extract information from a ad page
        :param ad_url:
        :param ad_page:
        :return:
        """
        pass
