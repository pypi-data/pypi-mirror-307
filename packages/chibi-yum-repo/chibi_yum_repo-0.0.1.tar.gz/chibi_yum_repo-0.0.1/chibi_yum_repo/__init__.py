# -*- coding: utf-8 -*-
from chibi.file import Chibi_file
from .repo import parse, to_string


__author__ = """dem4ply"""
__email__ = 'dem4ply@gmail.com'
__version__ = '0.0.1'


class Chibi_yum_repo( Chibi_file ):
    def read( self ):
        string = super().read()
        result = parse( string )
        return result

    def write( self, data ):
        result = to_string( data )
        super().write( result )
