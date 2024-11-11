![Ephemerista Logo](docs/logo.webp)

[![PyPI - Version](https://img.shields.io/pypi/v/ephemerista.svg)](https://pypi.org/project/ephemerista)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ephemerista.svg)](https://pypi.org/project/ephemerista)
[![coverage](https://gitlab.com/librespacefoundation/ephemerista/ephemerista-simulator/badges/main/coverage.svg?job=coverage)](https://librespacefoundation.gitlab.io/ephemerista/ephemerista-simulator/coverage)

---

<!-- start introduction -->

Ephemerista is an open source ([AGPLv3]-licensed) Python library for space mission design and analysis with a focus on telecommunications and constellation design.
The development of the first release of Ephemerista was [funded by the European Space Agency (ESA)][esa].

Ephemerista is being maintained by the [Libre Space Foundation][lsf].

[AGPLv3]: https://choosealicense.com/licenses/agpl-3.0/
[lsf]: https://libre.space
[esa]: https://connectivity.esa.int/projects/ossmisi

<!-- end introduction -->

## Features

<!-- start features -->

- Time scale and reference frame transformations
- Semi-analytical and numerical orbit propagation
- Event detection
- Spacecraft and ground asset modelling
- Communication systems modelling and link budgets analyses
- Constellation design and coverage analyses

<!-- end features -->

## Quickstart

<!-- start quickstart -->

Ephemerista is distributed on [PyPI] and can be installed via `pip`.

```shell
python -m venv .venv
source .venv/bin/activate
pip install ephemerista
```

Propagate the orbit of the ISS with Ephemerista.

```python
import ephemerista
from ephemerista.propagators.sgp4 import SGP4
from ephemerista.time import TimeDelta

# Load Earth Orientation Parameters
# See https://datacenter.iers.org/data/csv/finals2000A.all.csv
ephemerista.init_provider("finals2000A.all.csv")

# Propgate the trajectory
iss_tle = """ISS (ZARYA)
1 25544U 98067A   24187.33936543 -.00002171  00000+0 -30369-4 0  9995
2 25544  51.6384 225.3932 0010337  32.2603  75.0138 15.49573527461367"""

propagator = SGP4(tle=iss_tle)
start_time = propagator.time
end_time = start_time + TimeDelta.from_hours(6)
times = start_time.trange(end_time, step=float(TimeDelta.from_minutes(1)))
trajectory = propagator.propagate(times)
```

[PyPI]: https://pypi.org/project/ephemerista/

<!-- end quickstart -->

For more information, visit [Ephemerista's documentation][docs].

[docs]: https://docs.ephemerista.space

## Development

Please refer to [CONTRIBUTING.md](https://gitlab.com/librespacefoundation/ossmisi/ossmisi-simulator/-/blob/main/CONTRIBUTING.md).

## License

`ephemerista` is distributed under the terms of the [AGPLv3](https://spdx.org/licenses/AGPL-3.0-or-later.html) license.
