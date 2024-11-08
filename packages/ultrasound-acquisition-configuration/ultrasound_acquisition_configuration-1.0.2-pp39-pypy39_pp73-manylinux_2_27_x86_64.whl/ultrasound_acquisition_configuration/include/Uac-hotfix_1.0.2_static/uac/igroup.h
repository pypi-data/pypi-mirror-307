#pragma once

#include <algorithm>
#include <cstdint>
#include <memory>
#include <optional>
#include <vector>

#include <urx/detail/double_nan.h>

#include <uac/detail/compare.h>  // IWYU pragma: keep
#include <uac/hw_config.h>
#include <uac/trigger.h>
#include <uac/uac.h>

namespace uac {

struct DestinationLink;  // IWYU pragma: keep

struct IGroup {
  virtual bool operator==(const IGroup& other) const { return secureComparison(other, 0); }

  virtual ~IGroup() = 0;

  bool operator!=(const IGroup& other) const { return !operator==(other); }

  bool secureComparison(const IGroup& other, int recursion) const;

  urx::DoubleNan time_offset{0};

  std::optional<TriggerIn> trigger_in;

  std::optional<TriggerOut> trigger_out;

  uint32_t repetition_count = 0;

  std::vector<DestinationLink> destinations;

  urx::DoubleNan period;

  HwConfig hw_config;
};

}  // namespace uac

// NOLINTNEXTLINE(misc-header-include-cycle)
#include <uac/destination_link.h>  // IWYU pragma: keep

namespace uac {

// NOLINTNEXTLINE(misc-no-recursion)
inline bool IGroup::secureComparison(const IGroup& other, int recursion) const {
  return time_offset == other.time_offset && trigger_in == other.trigger_in &&
         trigger_out == other.trigger_out && repetition_count == other.repetition_count &&
         (recursion >= MAX_RECURSION ||
          std::equal(destinations.cbegin(), destinations.cend(), other.destinations.cbegin(),
                     other.destinations.cend(),
                     // NOLINTNEXTLINE(misc-no-recursion)
                     [recursion](const DestinationLink& dl1, const DestinationLink& dl2) {
                       return dl1.secureComparison(dl2, recursion + 1);
                     })) &&
         period == other.period && hw_config == other.hw_config;
}

inline IGroup::~IGroup() = default;

}  // namespace uac
