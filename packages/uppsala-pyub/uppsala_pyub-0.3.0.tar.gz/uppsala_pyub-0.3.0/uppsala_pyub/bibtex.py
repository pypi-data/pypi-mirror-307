from uppsala_pyub.handle_results import (
    fetch_namespace,
    get_yatt,
)
import re




def make_bibtex(xml_data, output_location='.'):
    ns = fetch_namespace()

    def _write_bibtex(bibtex, bibtex_key):
        with open(f"{output_location}/{bibtex_key}.bib", "w+") as out:
            bibtex = [f"{b},\n" if i < len(bibtex)-1 else f"{b}" for i, b in enumerate(bibtex)]
            [out.write(b) for b in bibtex]
            out.write("\n}")

    def _generate_key(author_list, year):
        lasts = [_.split(',')[0].replace(" ", "").strip() for _ in author_list]
        if len(lasts) == 1:
            key = lasts[0].lower() + year[:4]
        elif len(lasts) < 4:
            key = ''.join(lasts)+year[:4]
        else:
            key = lasts[0] + "EA" + year[:4]
        return key

    def _booktitle(bibtex):
        try:
            part_of = xml_data.find(f"{ns['xml']}display/{ns['xml']}ispartof").text
            assert part_of is not None
            assert part_of != ""
        except:
            return bibtex
        else:
            try:
                title, e, rest = re.split(r'\[(e|E)ds?\],', part_of)
            except:
                title = part_of
                e, rest = None, None
            for line in bibtex:
                if "    editor = {" in line:
                    editor = line.split("{")[1].strip("}")
                    for e in editor.split("AND"):
                        e = e.strip()
                        title.replace(e, "")
                    title.strip().strip("&").strip("and").strip().strip(",")
            bibtex.append(f"    booktitle = {{{title}}}")
            if rest is not None:
                pages = re.search(r'pp\s(\d{1,5}(-\d{1,5}))', rest)
                if pages is not None:
                    bibtex.append(f"   pages = {{{pages.group(1)}}}")
                plapub = re.search(r'(\S+:.*),', rest)
                if plapub is not None:
                    place, publisher = [_.strip() for _ in plapub.group(1).split(":")]
                    bibtex.append(f"    location = {{{place}}}")
                    bibtex.append(f"    publisher = {{{publisher}}}")
        return bibtex

    def _doi(bibtex):
        try:
            doi = xml_data.find(f"{ns['xml']}addata/{ns['xml']}doi").text
            assert doi is not None
            assert doi != ""
        except:
            return bibtex
        else:
            bibtex.append(f"    doi = {{{doi.strip()}}}")
        return bibtex

    def _editor(bibtex):
        try:
            editors = xml_data.find(f"{ns['xml']}display/{ns['xml']}contributor").text
            assert editors is not None
            assert editors is not None
        except:
            return bibtex
        else:
            editors = ' AND '.join([_.strip() for _ in editors.split(';')])
            bibtex.append(f"    editor = {{{editors.split()}}}")
        return bibtex

    def _isbn(bibtex):
        try:
            ISBN = xml_data.find(f"{ns['xml']}search/{ns['xml']}isbn").text
            assert ISBN is not None
            assert ISBN != ""
        except:
            try:
                identifier = xml_data.find(f"{ns['xml']}display/{ns['xml']}identifier").text
                m = re.search(r'\$\$CISBN\$V([\d-]+);', identifier)
                if m is not None:
                    ISBN = m.group(1)
                assert ISBN is not None
                assert ISBN != ""
            except:
                return bibtex
            else:
                bibtex.append(f"    isbn = {{{ISBN}}}")
        else:
            bibtex.append(f"    isbn = {{{ISBN}}}")
        return bibtex

    def _issue(bibtex):
        try:
            issue = xml_data.find(f"{ns['xml']}addata/{ns['xml']}issue").text
            assert issue is not None
            assert issue != ""
        except:
            return bibtex
        else:
            issue = re.sub(r'-{1}', "--", issue)
            bibtex.append(f"    issue = {{{issue.strip()}}}")
        return bibtex

    def _journal(bibtex):
        try:
            jtitle = xml_data.find(f"{ns['xml']}addata/{ns['xml']}jtitle").text
            assert jtitle is not None
            assert jtitle != ""
        except:
            return bibtex
        else:
            bibtex.append(f"    journal = {{{jtitle.strip()}}}")
        return bibtex

    def _pages(bibtex):
        try:
            pages = xml_data.find(f"{ns['xml']}addata/{ns['xml']}pages").text
            assert pages is not None
            assert pages != ""
        except:
            return bibtex
        else:
            pages = re.sub(r'-{1}', "--", pages)
            bibtex.append(f"    pages = {{{pages.strip()}}}")
        return bibtex

    def _place(bibtex):
        try:
            place = xml_data.find(f"{ns['xml']}display/{ns['xml']}place").text
            place = place.replace(":", "")
            place = place.strip()
            assert place is not None
            assert place != ''
        except:
            return bibtex
        else:
            bibtex.append(f"    location = {{{place}}}")
        return bibtex

    def _publisher(bibtex):
        for line in bibtex:
            if "    publisher = {" in line:
                return bibtex
        try:
            publisher = xml_data.find(f"{ns['xml']}display/{ns['xml']}publisher").text
            publisher = publisher.split(":")[-1]
            publisher = publisher.strip()
            assert publisher is not None
            assert publisher != ""
        except:
            return bibtex
        else:
            bibtex.append(f"    publisher = {{{publisher}}}")
        return bibtex

    def _volume(bibtex):
        try:
            volume = xml_data.find(f"{ns['xml']}addata/{ns['xml']}volume").text
            assert volume is not None
            assert volume != ""
        except:
            return bibtex
        else:
            bibtex.append(f"    volume = {{{volume.strip()}}}")
        return bibtex


    resource_types = {
        "books": "book",
        "book": "book",
        "article": "article",
        "book_chapter": "incollection",
    }

    fields = {
        "book": [_publisher, _place, _isbn],
        "article": [_journal, _volume, _issue, _pages, _doi],
        "incollection": [_editor, _booktitle, _publisher, _place, _pages, _isbn],
    }

    year, author_list, title, resource_type = get_yatt(xml_data, ns)
    bibtex = []
    if resource_type not in resource_types:
        raise ValueError(f"Unknown resource type {resource_type}. Select from {resource_types}.")

    rt = resource_types[resource_type]

    bibtex_key = _generate_key(author_list, year)
    bibtex.append(f"@{resource_types[resource_type]}" + "{" f"{bibtex_key}")
    bibtex.append(f"    title = {{{title.strip()}}}")
    bibtex.append(f"    year = {{{year[:4]}}}")
    bibtex.append(f"    author = {{{' AND '.join(author_list)}}}")
    for field in fields[rt]:
    #    print(field.__qualname__)
        bibtex = field(bibtex)
    #    print(bibtex)

    _write_bibtex(bibtex, bibtex_key)
    return bibtex_key


