#!/usr/bin/python
# -*- coding: iso8859-1 -*-

# *****************************************************************************
#
# "Open source" kit for CM-CIC P@iement (TM)
# 
# File "CMCIC_Tpe.py":
# 
# Author   : Euro-Information/e-Commerce (contact: centrecom@e-i.com)
# Version  : 1.04
# Date     : 01/01/2009
# 
# Copyright: (c) 2009 Euro-Information. All rights reserved.
# License  : see attached document "License.txt".
# 
# *****************************************************************************/

import sys, hmac, sha 

# Warning !! CMCIC_Config contains the key, you have to protect this file with all the mechanism available in your development environment.
# You may for instance put this file in another directory and/or change its name. If so, don't forget to adapt the import path below. 
from CMCIC_config import *

CMCIC_URLPAIEMENT = "paiement.cgi"

class CMCIC_Tpe :

        def __init__(self, sLang = "FR") :

                self._checkTpeParams()

                self.sVersion = CMCIC_VERSION
                self._sCle = CMCIC_CLE
                self.sNumero = CMCIC_TPE
                self.sUrlPaiement = CMCIC_SERVEUR + CMCIC_URLPAIEMENT

                self.sCodeSociete = CMCIC_CODESOCIETE
                self.sLangue = sLang

                self.sUrlOk = CMCIC_URLOK
                self.sUrlKo = CMCIC_URLKO

        def _checkTpeParams(self):

                try :
                        sParam = "CMCIC_CLE"
                        CMCIC_CLE
                        sParam = "CMCIC_VERSION"
                        CMCIC_VERSION
                        sParam = "CMCIC_TPE"
                        CMCIC_TPE
                        sParam = "CMCIC_CODESOCIETE"
                        CMCIC_CODESOCIETE
                except NameError:
                        print "Erreur paramètre "+ sParam  +" indéfini"
                        sys.exit(1)


class CMCIC_Hmac :

        def __init__(self, oTpe):

                self._sUsableKey = self._getUsableKey(oTpe)

        def computeHMACSHA1(self, sData):

                return self.hmac_sha1(self._sUsableKey, sData)

        def hmac_sha1(self, sKey, sData) :

                #HMAC = hmac.HMAC(sKey,None,hashlib.sha1)
                HMAC = hmac.HMAC(sKey,None,sha)
                HMAC.update(sData)

                return HMAC.hexdigest()

        def bIsValidHmac(self, sChaine, sMAC):

                return self.computeHMACSHA1(sChaine) == sMAC.lower()
                
        def _getUsableKey(self, oTpe) :

                hexStrKey  = oTpe._sCle[0:38]
                hexFinal   = oTpe._sCle[38:40] + "00";

                cca0=ord(hexFinal[0:1])

                if cca0>70 and cca0<97 :
                        hexStrKey += chr(cca0-23) + hexFinal[1:2]
                elif hexFinal[1:2] == "M" :
                        hexStrKey += hexFinal[0:1] + "0" 
                else :
                        hexStrKey += hexFinal[0:2]

                import encodings.hex_codec
                c =  encodings.hex_codec.Codec()
                hexStrKey = c.decode(hexStrKey)[0]

                return hexStrKey

