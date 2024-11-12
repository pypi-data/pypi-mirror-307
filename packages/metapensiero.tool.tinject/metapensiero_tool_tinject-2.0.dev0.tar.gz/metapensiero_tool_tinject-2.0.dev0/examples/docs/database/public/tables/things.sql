-- -*- coding: utf-8; sql-product: postgres -*-
-- :Project:   package.qualified.name -- Structure of table public.things
-- :Created:   lun 11 nov 2024 12:10:44 CET
-- :Author:    Lele Gaifax <lele@example.com>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2024 Lele Gaifax
--

CREATE TABLE public.things (
    field somedomain_t
  , other otherdomain_t

  , PRIMARY KEY (id) -- inherited from public.TimeStamped
) INHERITS (public.TimeStamped)
