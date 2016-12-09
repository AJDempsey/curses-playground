#!/usr/bin/env python3
"""snippet_ready.py: Read Snippet in XML form
"""
__author__ = 'colin@doch.org.uk'

# Require xml and argparse
import sys
import argparse
from xml.dom.minidom import parse, Node
from snippet import Snippet

def remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                # Cleanout any empty lines
                x.nodeValue = x.nodeValue.strip()
                x.nodeValue = x.nodeValue.rstrip('\n')
                if '' == x.nodeValue:
                    node.removeChild(x)
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)

def handleSnippetsXML(dom):

    snippets = dom.getElementsByTagName("snippet")
    for snippet in snippets:
        handleSnippet(dom, snippet)

def handleSnippet(dom, snippet):
    for child in snippet.childNodes:
        if child.nodeType == Node.TEXT_NODE:
            print("\"%s\"" % child.nodeValue)
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName != 'text':
                print(child.tagName)
            if child.hasChildNodes:
                remove_blanks(child)
                handleSnippet(dom, child)
                if child.tagName == "list":
                    print("list_end")

def snippet_read(xml_file):
    if xml_file:
        dom = parse(xml_file)
        remove_blanks(dom)
        handleSnippetsXML(dom)
        return []
    else:
        exit(1)

def main():
    # Start by parsing and sanity checking all input.

    parser = argparse.ArgumentParser(description='Parse XML for snippet')
    parser.add_argument('--xml', '-f', dest='xml',
                        help="The XML file")

    args = parser.parse_args()
    xml = args.xml

    stream = snippet_read(xml)

if __name__ == "__main__":
    main()
