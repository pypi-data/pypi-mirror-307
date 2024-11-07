
ansar-connect
=============

The **ansar-connect** library implements clear and concise network messaging for a wide range
of networking requirements. From multi-processing within a single host through to messaging
beween different LANs on the Internet. There is a single send method that does it all.

Features
--------

- Implements bi-directional, asynchronous network messaging,
- Provides a synchronous request-response layer,
- Inherits the data sophistication of **ansar.encode**,
- Seamlessly extends the asynchronous runtime from **ansar.create**, to span local and wide-area networks.


Changelog
=========

1.1.21 (2024-09-09)
-------------------

- Better data entry around update procedures.

- Clean org of api into crud groups.

- Finalize behaviour of overlay function.

- Support for refactor of cloud to use GroupTable.

1.1.3 (2024-09-22)
------------------

- Add HTTP integration

- Fix the teardown and reconnect of pub-sub sessions after keep-alive close

1.0.6 (2024-06-19)
------------------

- Fix handling of --main-role in abort scenarios

- Additions to docs - Odds And Ends, Dining Philosphers

- Implement self-checking of transports - directories and peers

- Fix/remove typos in comments

1.0 (2024-05-27)
----------------

- Implement standard listen and connect

- Implement publish and subscribe

- Create **ansar-host** and **ansar-lan** services

- Launch **ansar-wan** cloud service

- Complete **ansar-connect** docs
