import time
import re
from scrapeanything.types.webscraper import Props, Types, Functions
from scrapeanything.utils.type_utils import TypeUtils

class Scraper:

    def __del__(self) -> None:
        self.on_close()

    def wget(self, url: str, tries: int=0) -> None:
        self.parser = self.on_wget(url=url)

        try:
            if url is not None and tries < 3:
                self.parser = self.on_wget(url)
            
        except Exception as ex:
            tries += 1
            time.sleep(3)
            self.wget(url, tries)

    def xPath(self, path: str, element: any=None, pos: int=0, data_type: str=None, prop: str=None, explode=None, condition=None, substring=None, transform=None, replace=None, join=None, timeout: int=0, is_error: bool=True):       
        if path is None or path == '':
            return None

        element = self.parser if element is None else element
        el = self.on_xPath(element=element, path=path, timeout=timeout, is_error=is_error)

        # step 1: extract xpath
        if el is None or (el is not None and type(el) == list and len(el) == 0):
            return None

        elif isinstance(el, list) == True and data_type == Types.LIST:
            if pos == 0 or len(el) == 1:
                el = el[0]
                
        if isinstance(el, list) == False:
            el = [ el ]

        response = []
        for item in el:
            try:               
                if prop == Props.TEXT:
                    response.append(self.on_get_text(item))
                elif prop == Props.HTML:
                    response.append(self.on_get_html(item))
                elif prop is not None:
                    response.append(self.on_get_attribute(item, prop))
                else:
                    response.append(item)
            except Exception as e:
                pass

        if data_type == Types.LIST and type(el) is not list:
            return [ el ]
        # elif data_type == Types.LIST and type(el) is list:
        #     return el
        elif len(response) == 1 and data_type != Types.LIST:
            el = response[0]
        elif len(response) == 1 and data_type == Types.LIST:
            el = response
        elif pos is not None and len(response) > 1:
            el = response[pos]
        else:
            el = response

        primitive = (int, str, bool)
        if el is not None and (not isinstance(el, primitive) or not isinstance(el, primitive)):
            return el

        # step 2: apply functions
        options = dict(locals())
        for option in options:

            if option == Functions.SUBSTRING and substring is not None:
                el = self.substring(el, substring)
            if (option == Functions.EXPLODE) and explode is not None:
                el = self.explode(el, explode)
            if option == Functions.REPLACE and replace is not None:
                el = self.replace(el, replace)
            if option == Functions.JOIN and join is not None:
                el = self.join(el, join)

        # step 3 apply dataTypes
        if data_type is not None and '[' in data_type: # in the case dataType is a datetime with format (DATE[%Y-%m-%d %H:%M:%S])
            tokens = data_type.split('[')
            data_type = tokens[0]
            format = tokens[1][:-1]

        if data_type == Types.DATE:
            el = TypeUtils.to_date(el, format=format)
        if data_type == Types.PERCENTAGE:
            el = TypeUtils.to_number(el.replace('%', ''))
        if data_type == Types.BOOL:
            el = self.eval_condition(el, condition)
        if data_type == Types.MONEY:
            el = TypeUtils.to_money(el)
        if data_type == Types.NUMBER:
            el = TypeUtils.to_number(el)
        if data_type == Types.INTEGER:
            el = TypeUtils.to_integer(el)
        if data_type == Types.GEO:
            el = TypeUtils.to_geo(el)
        if data_type == Types.CHAR:
            el = TypeUtils.to_char(el)
        if data_type == Types.URL:
            base_url = TypeUtils.to_base_web(self.publisher.url)
            el = TypeUtils.to_normalized_url(base_url, el)

        if transform is not None:
            el = self.transform(el, transform)

        # clean string if element is not of ay complex type (WebElement, any object type, ...)
        primitive = (str) # (int, str, bool)
        if el is not None and isinstance(el, primitive):
            el = el.replace('\n', '').strip()

        return el

    def exists(self, path: str, element: any=None, timeout: int=0, is_error: bool=False):
        return self.on_exists(path=path, element=element, timeout=timeout, is_error=is_error)

    def substring(self, el: any, substring: str):
        if substring is not None and el is not None:
            idx_separator1 = None
            idx_separator2 = None

            index = [m.start() for m in re.finditer('"', substring)][1]
            separator1 = substring[:index+1].replace('"', '', 9999).strip()
            separator2 = substring[index+2:].replace('"', '', 9999).strip()

            idx_separator1 = el.index(separator1) + len(separator1)
            idx_separator2 = el.index(separator2)

            if idx_separator1 is not None and idx_separator2 is not None:
                el = el[idx_separator1:idx_separator2]

        return el       

    def explode(self, el, explode):
        '''
        Description:
        Arguments:
        Returns:
        '''
        
        tokens = []
        separator_find = None
        separator_replace = None

        if explode is not None and el is not None:
            separators, indexes = explode.rsplit(',', 1)

            separators = separators.split(';')

            separator_find = separators[0].strip(' ').replace('"', '', 9999)
            if len(separators) > 1:
                separator_replace = separators[1].strip(' ').replace('"', '', 9999)


            for index in indexes.split(';'):
                index = int(index.strip(' '))
                if el is not None and separator_find in el:
                    el = el.split(separator_find)[index]
                else:
                    el = ''
                
                tokens.append(el)

        if separator_replace is None:
            separator_replace = ' '
        
        return separator_replace.join(tokens).strip(' ')

    def replace(self, el: any, replace: str):
        elements = []

        if replace is not None and el is not None:
            groups = replace.replace('; ', ';').split(';')
            for i, group in enumerate(groups):
                replace = group.replace(', ', ',')
                tokens = [ token.replace('"', '') for token in replace.split(',') ]
                
                el = el.replace(tokens[0], tokens[1])
                
        return el

    def join(self, el: any, separator: str):
        if type(el) is list and separator is not None and separator != '':
            el =  [ e for e in el if e is not None and e != '' ]
            return separator.join(el)
        else:
            return el

    def transform(self, el, transform):
        return el

        if transform is not None and el is not None:
            for couple in transform:
                from_value, to_value = couple
            return el # TODO
        else:
            return el

    def eval_condition(self, element, condition):
        return eval('element ' + condition)
        '''
        try:
            return eval('int(element) ' + condition)
        except Exception as e:
            return eval('element ' + condition)
        '''

    def hover(self, path: str, element: any=None, is_error: bool=True, timeout: int=0) -> None:
        self.on_hover(path=path, element=element, is_error=is_error, timeout=timeout)

    def enter_text(self, path: str, text: str, element: any=None, clear: bool=False, timeout: int=0, is_error: bool=False):
        return self.on_enter_text(path=path, text=text, element=element, clear=clear, timeout=timeout, is_error=is_error)

    def click(self, path: str, element: any=None, timeout: int=0, pos: int=0, is_error: bool=True) -> None:
        self.on_click(path=path, element=element, timeout=timeout, pos=pos, is_error=is_error)

    def click_and_hold(self, path: str, seconds: float, element: any=None, timeout: int=0, is_error: bool=True) -> None:
        self.on_click_and_hold(path=path, seconds=seconds, element=element, timeout=timeout, is_error=is_error)

    def back(self):
        self.on_back()

    def get_current_url(self):
        return self.on_get_current_url()

    def solve_captcha(self, path):
        self.on_solve_captcha(path)

    def get_css(self, element: any, prop: str) -> str:
        return self.on_get_css(element.scraper.parser, prop)

    def login(self, username_text=None, username=None, password_text=None, password=None):
        return self.on_login(username_text, username, password_text, password)

    def search(self, path: str=None, text: str=None, timeout: int=0):
        return self.on_search(path=path, text=text, timeout=timeout)

    def scroll_to_bottom(self):
        return self.on_scroll_to_bottom()

    def get_scroll_top(self):
        return self.on_get_scroll_top()

    def get_scroll_bottom(self):
        return self.on_get_scroll_bottom()

    def select(self, path: str, option: str) -> None:
        self.on_select(path=path, option=option)

    def get_image_from_canvas(self, path: str, local_path: str, element: any) -> str:
        return self.on_get_image_from_canvas(path=path, local_path=local_path, element=element)

    def switch_to(self, element: any) -> None:
        return self.on_switch_to(element=element)

    def screenshot(self, file: str) -> None:
        self.on_screenshot(file=file)

    def freeze(self) -> None:
        self.on_freeze()

    def unfreeze(self) -> None:
        self.on_unfreeze()
        
    def get_cookies(self) -> 'list[dict]':
        return self.on_get_cookies()

    def close(self):
        self.on_close()