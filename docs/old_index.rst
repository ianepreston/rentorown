Rent or Own Calculator
========================================================
A rent or own calculator based to the best of my abilities on Canadian data.

IMPORTANT DISCLAIMER
=================================
The calculations and results of this code are presented without any warranty. Don't make
a huge financial decision based off some code you found on the internet. While I've done
my best to make a good model, I've made a number of assumptions about the structure
of the problem. On top of that, the model itself requires entering a number of assumptions.
The model can only be said to be accurate if the calculations are correct, the structure
of the problem is correct, and the assumptions that the user enters to specify their exact
comparison are correct. I made this as a model to organize my thinking about the tradeoffs
of renting vs owning a home, and have made efforts to make it accurate, but I can't offer
any guarantees to its validity, and assume no responsibility for any financial decisions
anyone might make in whole or in part due to its results. Hope that covers my ass.

Key classes and functions documentation
==========================================

.. autoclass:: rentorown.house.House
   :members:


.. autoclass:: rentorown.house.Mortgage
   :members:

.. autofunction:: rentorown.asset.annual_to_monthly_return

.. autofunction:: rentorown.asset.annual_to_monthly_stdev

.. autoclass:: rentorown.asset.BaseAsset

.. autoclass:: rentorown.rentorown.RentOrOwn
    :members:

.. autoclass:: rentorown.rentorown.ParameterizedRentOrOwn
    :members:



Indices and tables
==================

* :ref:`modindex`
