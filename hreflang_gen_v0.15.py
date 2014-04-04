from xml.etree import ElementTree
ElementTree.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ElementTree.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
print 'HREFLANG XML Sitemap Generator v0.15 by Paul Shapiro\n'
finput = raw_input('Please specify the file path to your source xml sitemap:\n')
doc = ElementTree.parse(open(finput))
root = doc.getroot()
root.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
nparts = int(input('How many parts of the URL do you want to replace:\n'))
nlangs = int(input('How many languages:\n'))
lang_replacements = dict()
matches = []
for i in xrange(nparts):
    matches.append(raw_input('please input a part of the URL you want to replace:\n'))

for i in xrange(nlangs):
    langcode = raw_input('Please enter the #' + str(i + 1) + ' language code:\n')
    replacements = []
    for i in xrange(nparts):
        replace_match = matches[i]
        replace_with = raw_input('what would you like to replace ' + matches[i] + ' with?:\n')
        replacements.append((replace_match, replace_with))

    lang_replacements[langcode] = replacements

for el in doc.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    url = el.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    for (langcode, replacements,) in lang_replacements.iteritems():
        localized_url = url
        for replacement_tuple in replacements:
            localized_url = localized_url.replace(replacement_tuple[0], replacement_tuple[1])

        ElementTree.SubElement(el, 'xhtml:link', {'rel': 'alternate',
         'hreflang': langcode,
         'href': localized_url})
         
def indent(elem, level = 0):
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

indent(root)
foutput = raw_input('choose a filename to save output as *.xml \n')
tree = ElementTree.ElementTree(root)
tree.write(foutput)
f = open(foutput, 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + ElementTree.tostring(root))
f.close()