#!/usr/bin/env python3
"""snippet_ready.py: Read Snippet in XML form
"""
__author__ = 'colin@doch.org.uk'

# Require xml and argparse
import sys
import argparse
from xml.dom.minidom import parse, Node

def remove_all(node):
    while len(node.childNodes) > 0:
        child = node.firstChild
        node.removeChild(child)
        remove_all(node)

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

def handleSnippetXML(dom):

    snippets = dom.getElementsByTagName("snippet")
    for snippet in snippets:
        handleSnippet(dom, snippet)

def handleSnippet(dom, snippet):
    for child in snippet.childNodes:
        print(child.tagName)

def main():
    # Start by parsing and sanity checking all input.

    parser = argparse.ArgumentParser(description='Parse XML for snippet')
    parser.add_argument('--xml', '-f', dest='xml',
                        help="The XML file")

    args = parser.parse_args()
    xml = args.xml

    if xml:
        dom = parse(xml)
        remove_blanks(dom)
        handleSnippetXML(dom)

if __name__ == "__main__":
    main()
