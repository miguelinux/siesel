# CXL Features

## Linux v6.10

* commit 940325add1c54e3018277d6d783ec419262729e8

   > cxl/mbox: Add Get Log Capabilities and Get Supported Logs Sub-List commands
   >
   > Adding UAPI support for
   > 1. CXL r3.1 8.2.9.5.3 Get Log Capabilities.
   > 2. CXL r3.1 8.2.9.5.6 Get Supported Logs Sub-List.

* commit 206f9fa9d55592c8cea0ccf84a5242b7c7cf3748

   > cxl/mbox: Add Clear Log mailbox command
   >
   > Adding UAPI support for CXL r3.1 8.2.9.5.4
   > Clear Log command.
   >
   > This proposed patch will be useful for clearing and populating
   > the Vendor debug log in certain scenarios, allowing for the
   > aggregation of results over time.

* commit 54e8dd59a76c031317eef61fef93f01d4e76fd3e

   > cxl/hdm: Add debug message for invalid interleave granularity
   >
   > There's no debug message for invalid interleave granularity.  This
   > makes it hard to debug related bugs.  So, this is added in this patch.

## Linux v6.11

* commit 675e979db473d08be346a3190c5f0db095a57153

    cxl/events: Use a common struct for DRAM and General Media events

    > cxl_event_common was an unfortunate naming choice and caused confusion with
    > the existing Common Event Record. Furthermore, its fields didn't map all
    > the common information between DRAM and General Media Events.
    >
    > Remove cxl_event_common and introduce cxl_event_media_hdr to record common
    > information between DRAM and General Media events.
    >
    > cxl_event_media_hdr, which is embedded in both cxl_event_gen_media and
    > cxl_event_dram, leverages the commonalities between the two events to
    > simplify their respective handling.

* commit a0caa19711ceb54c34368f66a746844fb03fde6c

    cxl: add missing MODULE_DESCRIPTION() macros

    > make allmodconfig && make W=1 C=1 reports:
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/core/cxl_core.o
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/cxl_pci.o
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/cxl_mem.o
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/cxl_acpi.o
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/cxl_pmem.o
    > WARNING: modpost: missing MODULE_DESCRIPTION() in drivers/cxl/cxl_port.o
    >
    > Add the missing invocations of the MODULE_DESCRIPTION() macro.

* commit a3483ee7e6a7f2d12b5950246f4e0ef94f4a5df0

    cxl/region: Fix a race condition in memory hotplug notifier

    > In the memory hotplug notifier function of the CXL region,
    > cxl_region_perf_attrs_callback(), the node ID is obtained by checking
    > the host address range of the region. However, the address range
    > information is not available when the region is registered in
    > devm_cxl_add_region(). Additionally, this information may be removed
    > or added under the protection of cxl_region_rwsem during runtime. If
    > the memory notifier is called for nodes other than that backed by the
    > region, a race condition may occur, potentially leading to a NULL
    > dereference or an invalid address range.
    >
    > The race condition is addressed by checking the availability of the
    > address range information under the protection of cxl_region_rwsem. To
    > enhance code readability and use guard(), the relevant code has been
    > moved into a newly added function: cxl_region_nid().


