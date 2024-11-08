#pragma once

#include <memory>
#include <optional>

#include <uac/detail/compare.h>  // IWYU pragma: keep
#include <uac/trigger.h>
#include <uac/uac.h>

namespace uac {

struct IGroup;  // IWYU pragma: keep

struct DestinationLink {
  bool operator==(const DestinationLink& other) const { return secureComparison(other, 0); }

  bool operator!=(const DestinationLink& other) const { return !operator==(other); }

  bool secureComparison(const DestinationLink& other, int recursion) const;

  std::optional<TriggerIn> trigger;

  std::weak_ptr<IGroup> destination;
};

}  // namespace uac

// NOLINTNEXTLINE(misc-header-include-cycle)
#include <uac/igroup.h>  // IWYU pragma: keep

namespace uac {

// NOLINTNEXTLINE(misc-no-recursion)
inline bool DestinationLink::secureComparison(const DestinationLink& other, int recursion) const {
  auto lhs_lock = destination.lock();
  auto rhs_lock = other.destination.lock();
  return trigger == other.trigger && (recursion >= MAX_RECURSION || (lhs_lock && rhs_lock)
                                          ? (lhs_lock->secureComparison(*rhs_lock, recursion + 1))
                                          : (!!lhs_lock == !!rhs_lock));
}

}  // namespace uac
