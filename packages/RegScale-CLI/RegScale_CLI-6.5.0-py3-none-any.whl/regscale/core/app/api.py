#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard imports """

import concurrent.futures
import logging
import os
import re
import sys
import warnings
from typing import List, Optional, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from regscale.core.app.application import Application

import requests
from requests.adapters import HTTPAdapter, Retry
from rich.progress import Progress


logger = logging.getLogger("rich")


class Api:
    """Wrapper for interacting with the RegScale API

    :param Optional[Application] app: Application object, defaults to None
    :param int timeout: timeout for API calls, defaults to 10
    :param Union[int, str] retry: number of retries for API calls, defaults to 5
    """

    _app: "Application"
    app: "Application"

    def __init__(
        self,
        app: Optional["Application"] = None,
        timeout: int = int(os.getenv("REGSCALE_TIMEOUT", 10)),
        retry: int = 5,
    ):
        from regscale.core.app.application import Application

        if app:
            import warnings

            warnings.warn(
                "The API class no longer requires Application object. Use 'Api()' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if isinstance(timeout, str):
            timeout = int(timeout)
        self.timeout = timeout
        self.accept = "application/json"
        self.content_type = "application/json"
        r_session = requests.Session()
        self.pool_connections = 200
        self.pool_maxsize = 200
        self.retries = Retry(total=retry, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.auth = None
        super().__init__()
        self.app = Application()
        self.logger = logger
        if self.config and "ssl_verify" in self.config:
            r_session.verify = self.config["ssl_verify"]
        if self.config and "timeout" in self.config:
            self.timeout = self.config["timeout"]
        # get the user's domain prefix eg https:// or http://
        domain = self.config.get("domain") or self.app.retrieve_domain()
        domain = domain[: (domain.find("://") + 3)]
        r_session.mount(
            domain,
            HTTPAdapter(
                max_retries=self.retries,
                pool_connections=self.pool_connections,
                pool_maxsize=self.pool_maxsize,
                pool_block=True,
            ),
        )
        self.session = r_session

    @property
    def config(self) -> dict:
        """
        Get the application config

        :return: Application config
        :rtype: dict
        """
        return self.app.config

    def update_attributes_from_config(self):
        """
        Update attributes from the application config
        """
        r_session = requests.Session()
        if self.config and "ssl_verify" in self.config:
            r_session.verify = self.config["ssl_verify"]
        if self.config and "timeout" in self.config:
            self.timeout = self.config["timeout"]
        # get the user's domain prefix eg https:// or http://
        domain = self.config.get("domain") or self._app.retrieve_domain()
        domain = domain[: (domain.find("://") + 3)]
        r_session.mount(
            domain,
            HTTPAdapter(
                max_retries=self.retries,
                pool_connections=self.pool_connections,
                pool_maxsize=self.pool_maxsize,
                pool_block=True,
            ),
        )
        self.session = r_session

    def get(
        self,
        url: str,
        headers: Optional[dict] = None,
        params: Optional[Union[list, Tuple]] = None,
    ) -> Optional[requests.models.Response]:
        """
        Get Request for API

        :param str url: URL for API call
        :param dict headers: headers for the api get call, defaults to None
        :param Optional[Union[list, Tuple]] params: Any parameters for the API call, defaults to None
        :return: Requests response
        :rtype: Optional[requests.models.Response]
        """
        url = normalize_url(url)
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
                "Content-Type": self.content_type,
            }
        # if response fails to assign, the log error will fail anyway
        # FIXME - should this be handled here or in `self.session.get`?
        response = None
        try:
            response = self.session.get(
                url=url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
        except requests.exceptions.ConnectionError:
            logger.error("Unable to connect to: %s Please verify the URL and try again.", url, exc_info=True)
            return response
        except requests.exceptions.RequestException:
            logger.error(
                "Received unexpected response from %s\nStatus code %s: %s",
                url,
                getattr(response, "status_code", "None"),
                getattr(response, "text", "None"),
                exc_info=True,
            )
            sys.exit(1)
        return response

    def delete(self, url: str, headers: Optional[dict] = None) -> requests.models.Response:
        """
        Delete data using API

        :param str url: URL for the API call
        :param Optional[dict] headers: headers for the API call, defaults to None
        :return: API response
        :rtype: requests.models.Response
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
            }
        return self.session.delete(url=normalize_url(url), headers=headers)

    def post(
        self,
        url: str,
        headers: Optional[dict] = None,
        json: Optional[Union[dict, str, list]] = None,
        data: Optional[dict] = None,
        files: Optional[list] = None,
        params=None,
    ) -> requests.models.Response:
        """
        Post data to API

        :param str url: URL for the API call
        :param dict headers: Headers for the API call, defaults to None
        :param Optional[Union[dict, str, list]] json: Dictionary of data for the API call, defaults to None
        :param dict data: Dictionary of data for the API call, defaults to None
        :param list files: Files to post during API call, defaults to None
        :param params: Any parameters for the API call, defaults to None
        :return: API response
        :rtype: requests.models.Response
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            try:
                headers = {
                    "Authorization": self.config["token"],
                }
            except KeyError as kex:
                self.config["token"] = "Please Enter Token"
                self.app.save_config(self.config)
                self.logger.error(
                    "Token not found in init.yaml, but we have added it. Please login again.\n%s",
                    kex,
                )
        if not json and data:
            response = self.session.post(
                url=normalize_url(url),
                headers=headers,
                data=data,
                files=files,
                params=params,
                timeout=self.timeout,
            )
        else:
            response = self.session.post(
                url=normalize_url(url),
                headers=headers,
                json=json,
                files=files,
                params=params,
                timeout=self.timeout,
            )
        logger.debug("URL: %s, data: %s", url, json)
        return response

    def put(
        self,
        url: str,
        headers: Optional[dict] = None,
        json: Optional[Union[dict, List[dict]]] = None,
        params: Optional[Union[list, Tuple]] = None,
    ) -> requests.models.Response:
        """
        Update data via API call

        :param str url: URL for the API call
        :param Optional[dict] headers: Headers for the API call, defaults to None
        :param Optional[Union[dict, List[dict]]] json: Dictionary of data for the API call, defaults to None
        :param Optional[Union[list, Tuple]] params: Any parameters for the API call, defaults to None
        :return: API response
        :rtype: requests.models.Response
        """
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
            }
        response = self.session.put(
            url=normalize_url(url),
            headers=headers,
            json=json,
            params=params,
            timeout=self.timeout,
        )
        logger.debug(response.text)
        return response

    def graph(
        self, query: str, url: Optional[str] = None, headers: Optional[dict] = None, res_data: Optional[dict] = None
    ) -> dict:
        """
        Execute GraphQL query and handles pagination before returning the data to the API call

        :param str query: the GraphQL query to execute
        :param Optional[str] url: URL for the API call, defaults to None
        :param Optional[dict] headers: Headers for the API call, defaults to None
        :param Optional[dict] res_data: dictionary of data from GraphQL response, only used during pagination & recursion
        :return: Dictionary response from GraphQL API
        :rtype: dict
        """
        logger.debug("STARTING NEW GRAPH CALL")
        logger.debug("=" * 50)
        response_data = {}
        pagination_flag = False
        # change the timeout to match the timeout of the GraphQL timeout in the application
        self.timeout = 90
        if self.auth:
            self.session.auth = self.auth
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "Accept": self.accept,
                "Content-Type": self.content_type,
            }
        # check the query if skip was provided, if not add it for pagination
        if "skip" not in query:
            query = query.replace("(", "(skip: 0\n")
        # set the url for the query
        url = normalize_url(f'{self.config["domain"]}/graphql' if url is None else url)
        logger.debug(f"{url=}")
        logger.debug(f"{query=}")
        # make the API call
        response = self.session.post(
            url=normalize_url(url),
            headers=headers,
            json={"query": query},
            timeout=self.timeout,
        )
        logger.debug(f"{response.text=}")
        try:
            response_json = response.json()
            if "errors" in response_json:
                logger.error("GraphQL query returned errors:")
                for error in response_json["errors"]:
                    logger.error(f"Message: {error.get('message')}")
                    logger.error(f"Locations: {error.get('locations')}")
                    logger.error(f"Path: {error.get('path')}")
                logger.error(f"Query that caused the error: {query}", exc_info=True)
                return {}  # Return an empty dict instead of exiting
            # convert response to JSON object
            response_data = response_json["data"]
            logger.debug(f"{response_data=}")
            # iterate through and add it to the res_data if needed
            for key, value in response_data.items():
                # add the new API response data to the data from previous call
                if res_data:
                    res_data[key]["items"].extend(response_data[key]["items"])
                # check if pagination required
                try:
                    if value.get("pageInfo").get("hasNextPage") is True and not pagination_flag:
                        # set pagination_flag to true
                        pagination_flag = True
                        # find the location of the old skip in the query and parse the int after it
                        old_skip_match = re.search(r"skip: (\d+)", query)
                        if old_skip_match:
                            old_skip = int(old_skip_match.group(1))

                            # set the new value of the skip using old + # of items returned
                            new_skip = old_skip + len(response_data[key]["items"])

                            # replace the old skip value with the new skip value that was calculated
                            query = query.replace(f"skip: {old_skip}", f"skip: {new_skip}")
                        else:
                            # If no skip found, add it to the beginning of the query
                            new_skip = len(response_data[key]["items"])
                            query = query.replace("(", f"(skip: {new_skip}\n", 1)

                        # if no previous pagination, break this loop
                        if not res_data:
                            break
                except (KeyError, AttributeError):
                    continue
        except requests.exceptions.JSONDecodeError as err:
            logger.error("Received JSONDecodeError!\n%s", err)
            logger.debug("%i: %s - %s", response.status_code, response.text, response.reason)
            return {}
        except KeyError as err:
            logger.error("No items were returned from %s!\n%s", url, err)
            logger.debug("%i: %s - %s", response.status_code, response.text, response.reason)
            return {}
        # check if already called for recursion
        # res_data: set data to pagination data
        # response_data: most recent API call
        data = res_data or response_data
        if pagination_flag:
            # recall the function with the new query and extend the data with the results
            response_data = self.graph(url=url, headers=headers, query=query, res_data=data)
            # set the data to the pagination data
            data = response_data
        # return the data
        return data

    def update_server(
        self,
        url: str,
        headers: Optional[dict] = None,
        json_list: Optional[list] = None,
        method: str = "post",
        config: Optional[dict] = None,
        message: str = "Working",
    ) -> None:
        """
        Concurrent Post or Put of multiple objects

        The 'update_server' method is deprecated, use 'RegScaleModel' create or update methods instead

        :param str url: URL for the API call
        :param Optional[dict] headers: Headers for the API call, defaults to None
        :param Optional[list] json_list: Dictionary of data for the API call, defaults to None
        :param str method: Method for API to use, defaults to "post"
        :param Optional[dict] config: Config for the API, defaults to None
        :param str message: Message to display in console, defaults to "Working"
        :rtype: None
        """
        warnings.warn(
            "The 'update_server' method is deprecated, use 'RegScaleModel' create or update methods instead",
            DeprecationWarning,
        )
        if headers is None and config:
            headers = {"Accept": "application/json", "Authorization": config["token"]}

        if json_list and len(json_list) > 0:
            with Progress(transient=False) as progress:
                task = progress.add_task(message, total=len(json_list))
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.config["maxThreads"]) as executor:
                    if method.lower() == "post":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(self.post, url, headers, x),
                                json_list,
                            )
                        )
                    if method.lower() == "put":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(self.put, f"{url}/{x['id']}", headers, x),
                                json_list,
                            )
                        )
                    if method.lower() == "delete":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(self.delete, f"{url}/{x['id']}", headers),
                                json_list,
                            )
                        )
                    for future in concurrent.futures.as_completed(result_futures):
                        try:
                            if future.result().status_code != 200:
                                logger.warning(
                                    "Status code is %s: %s from %s.",
                                    future.result().status_code,
                                    future.result().text,
                                    future.result().url,
                                )
                            progress.update(task, advance=1)
                        except Exception as ex:
                            logger.error("Error is %s, type: %s", ex, type(ex))


def normalize_url(url: str) -> str:
    """
    Function to remove extra slashes and trailing slash from a given URL

    :param str url: URL string normalize
    :return: A normalized URL
    :rtype: str
    """
    segments = url.split("/")
    correct_segments = [segment for segment in segments if segment != ""]
    first_segment = str(correct_segments[0])
    if "http" not in first_segment:
        correct_segments = ["http:"] + correct_segments
    correct_segments[0] = f"{correct_segments[0]}/"
    return "/".join(correct_segments)
