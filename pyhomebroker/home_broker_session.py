#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Home Broker API - Market data downloader
# https://github.com/crapher/pyhomebroker.git
#
# Copyright 2020 Diego Degese
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import urllib.parse

import httpx as rq
import pandas as pd
from pyquery import PyQuery as pq

from .common import SessionException, user_agent


class HomeBrokerSession:

    def __init__(self, broker, proxy_url=None):
        """
        Class constructor

        Parameters
        ----------
        broker : dictionary
            A broker dictionary with all the broker information. (Check brokers.py)
        proxy_url : str, optional
            The proxy URL with one of the following formats:
                - scheme://user:pass@hostname:port
                - scheme://user:pass@ip:port
                - scheme://hostname:port
                - scheme://ip:port

            Ex. https://john:doe@10.10.1.10:3128
        """

        self._proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
        self.broker = broker

        self.is_user_logged_in = False
        self.cookies = {}

        self.__ipaddress = None

########################
#### PUBLIC METHODS ####
########################
    async def login(self, dni, user, password, raise_exception=False):
        """
        This method authenticates the user in the home broker platform.

        Parameters
        ----------
        dni : int
            The national document identification of the user.
        user : str
            The username used in the platform.
        password : str
            The password used in the platform.
        raise_exception : bool
            If the method should raise an exception when an error happens.

        Raises
        ------
        pyhomebroker.exceptions.SessionException
            The user cannot be authenticated.
        requests.exceptions.HTTPError
            There is a problem related to the HTTP request.

        Returns
        -------
        True is the user authenticated successfully, otherwise False (if raise_exception is False).
        """

        try:
            headers = {
                'User-Agent': user_agent,
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            url = '{}/Login/Ingresar'.format(self.broker['page'])

            ip = await self.__get_ipaddress()
            
            payload = {
                'IpAddress': ip,
                'Dni': dni,
                'Usuario': user,
                'Password': password}
            payload = urllib.parse.urlencode(payload)

            async with rq.AsyncClient(proxies=self._proxies) as sess:
                response = await sess.post(url, data=payload, headers=headers)
                response.raise_for_status()

                doc = pq(response.text)
                if not doc('#usuarioLogueado'):

                    errormsg = doc('.callout-danger')
                    if errormsg:
                        raise SessionException(errormsg.text())

                    raise SessionException('Session cannot be created.  Check the entered information and try again.')

                self.is_user_logged_in = True
                self.cookies =  dict_from_cookiejar(sess.cookies)
        except Exception as ex:
            self.is_user_logged_in = False
            self.cookies = {}

            if raise_exception:
                raise

        return self.is_user_logged_in

    def logout(self):
        """
        This method cleans the login data in the library.
        """

        self.is_user_logged_in = False
        self.cookies = {}

#########################
#### PRIVATE METHODS ####
#########################
    async def __get_ipaddress(self):

        if not self.__ipaddress:
            async with rq.AsyncClient(proxies=self._proxies) as sess: 
                data = await sess.get('https://api.ipify.org/?format=json&callback=get_ip')
                self.__ipaddress = (data.json()['ip'])

        return self.__ipaddress

def dict_from_cookiejar(cj):
    pojo={}
    for c in cj:
        pojo[c]=cj[c]
    return pojo
