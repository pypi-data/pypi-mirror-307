====================
PDBNucleicAcids
====================


.. image:: https://img.shields.io/pypi/v/pdbnucleicacids.svg
        :target: https://pypi.python.org/pypi/pdbnucleicacids

.. image:: https://readthedocs.org/projects/pdbnucleicacids/badge/?version=latest
        :target: https://pdbnucleicacids.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/MorfeoRenai/pdbnucleicacids/shield.svg
     :target: https://pyup.io/repos/github/MorfeoRenai/pdbnucleicacids/
     :alt: Updates



A `Biopython <https://biopython.org/>`_ based package that constructs
and represent all nucleic acids in a PDB structure, with a special focus on
base-pair representation.


* Free software: MIT license
* Documentation: https://pdbnucleicacids.readthedocs.io.


Features
--------

* TODO


TODO
--------

* Add a module similar to Polypeptide from Biopython, but for nucleic acids, with

    * class Nucleic or NucleicAcid
    
    * class NucleicBuilder or NucleicAcidBuilder
    
    * class PairedNucleic or PairedNucleicAcid or DoubleStrandNucleic or DoubleStrandNucleicAcid

* regarding BasePairsRules:

    * Distinguish between DNA and RNA bases (i.e. Deodyribose Adenine can pair with both Deoxyribose Thyamine or Ribose Thyamine)

* Proper tests (WIP)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
