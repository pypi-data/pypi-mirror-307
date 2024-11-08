from starlette.responses import FileResponse

import cbr_website_beta
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from osbot_utils.utils.Files            import path_combine_safe


class CBR__WebC__Routes(Fast_API_Routes):
    tag: str = 'webc'

    def cbr_webc(self):
        file_webc = path_combine_safe(cbr_website_beta.path, 'apps/templates/pages/page-with-webc.html')
        return FileResponse(file_webc)

    def cbr_webc_dev(self, path=None):
        file_webc = path_combine_safe(cbr_website_beta.path, 'apps/templates/pages/page-with-webc-dev.html')
        return FileResponse(file_webc)

    def setup_routes(self):
        #self.add_route_get(self.cbr_webc)
        self.router.add_api_route(path='/cbr-webc'                , endpoint=self.cbr_webc, methods=['GET'])
        self.router.add_api_route(path='/cbr-webc/'               , endpoint=self.cbr_webc, methods=['GET'])
        self.router.add_api_route(path='/cbr-webc/{path:path}'    , endpoint=self.cbr_webc, methods=['GET'])
        self.router.add_api_route(path='/cbr-webc-dev'            , endpoint=self.cbr_webc_dev, methods=['GET'])
        self.router.add_api_route(path='/cbr-webc-dev/'           , endpoint=self.cbr_webc_dev, methods=['GET'])
        self.router.add_api_route(path='/cbr-webc-dev/{path:path}', endpoint=self.cbr_webc_dev, methods=['GET'])