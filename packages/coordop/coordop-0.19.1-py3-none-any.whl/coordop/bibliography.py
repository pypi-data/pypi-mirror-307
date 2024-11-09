from bibliograpy.api import *


MAP_PROJECTIONS = Book.generic(cite_key='map_projections',
                               editor='UNITED STATES GOVERNMENT PRINTING OFFICE, WASHINGTON',
                               publisher='',
                               title='Map Projections - A Working Manual',
                               year='1987',
                               non_standard=NonStandard(url='https://pubs.usgs.gov/pp/1395/report.pdf'),
                               scope=SHARED_SCOPE)

IOGP = Misc.generic(cite_key='iogp',
                    institution='IOGP',
                    title='International Association of Oil & Gas Producers',
                    scope=SHARED_SCOPE)

IOGP_GUIDANCE_NOTE_7_2_2019 = TechReport.generic(cite_key='iogp_guidance_note_7_2_2019',
                                                 author='',
                                                 crossref=IOGP,
                                                 number='373-7-2',
                                                 title='Geomatics Guidance Note 7, part 2 Coordinate Conversions & Transformations including Formulas',
                                                 type='document',
                                                 year='2019',
                                                 non_standard=NonStandard(url='https://www.iogp.org/wp-content/uploads/2019/09/373-07-02.pdf'),
                                                 scope=SHARED_SCOPE)
