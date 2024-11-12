# -*- coding: utf-8 -*-
import re
from chibi.snippet.iter import chunk_each
from chibi_atlas import Chibi_atlas


name_regex = re.compile( r'\[.*\]' )


def parse( content ):
    result = Chibi_atlas()
    lines = filter( bool, content.split( '\n' ) )
    chunks = chunk_each( lines, lambda x: name_regex.match( x ) )
    for section in chunks:
        section_key = section[0][1:-1].strip()
        section_data = section[1:]
        section_dict = Chibi_atlas()
        for line in section_data:
            key, value = line.split( '=', 1 )
            key = key.strip()
            value = value.strip()
            section_dict[ key ] = value
        result[ section_key ] = section_dict
    return result


def to_string( d ):
    result = "\n".join( map(
        lambda item: _transform_section( *item ),
        d.items() ) )
    return result


def _transform_section( name, section ):
    name = str( name ).strip()
    result = f"[{name}]\n"
    for k, v in section.items():
        result += f"{k}={v}\n"
    return result
