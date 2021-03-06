"""Discover Philips Hue bridges."""
from . import SSDPDiscoverable


class Discoverable(SSDPDiscoverable):
    """Add support for discovering Philips Hue bridges."""

    def info_from_entry(self, entry):
        """Return the most important info from a uPnP entry."""
        desc = entry.description

        return desc['device']['friendlyName'], desc['URLBase']

    def get_entries(self):
        """Get all the Hue bridge uPnP entries."""
        nupnp_entries = self.netdis.phue.entries

        # Hub models for year 2012 and 2015
        ssdp_entries = self.find_by_device_description({
            "manufacturer": "Royal Philips Electronics",
            "modelNumber": ["929000226503", "BSB002"]
        })

        return self.merge_entries(nupnp_entries, ssdp_entries)

    # pylint: disable=no-self-use
    def merge_entries(self, nupnp_entries, ssdp_entries):
        """Takes lists of device entries found using N-UPnP & SSDP lookups and
        merges them making sure that same device is only discoverd once.

        """
        entries = nupnp_entries

        for nupn_entry in entries:
            for ssdp_entry in ssdp_entries:
                url_base1 = nupn_entry.description['URLBase']
                url_base2 = ssdp_entry.description['URLBase']

                if url_base1 != url_base2:
                    entries.append(ssdp_entry)

        return entries
