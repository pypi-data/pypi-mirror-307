hardware_fragment = """
fragment HardwareFragment on Hardware {
  id
  pk
  name
  slug
  createdAt
  updatedAt
  isAvailable
  isOnline
  isQuarantined
  isHealthy
  capabilities {
    id
    pk
  }
  activeReservation {
    id
    pk
  }
}
"""
