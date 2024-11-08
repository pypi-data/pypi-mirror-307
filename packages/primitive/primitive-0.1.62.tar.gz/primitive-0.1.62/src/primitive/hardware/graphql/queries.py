from .fragments import hardware_fragment

hardware_list = (
    hardware_fragment
    + """

query hardwareList(
  $before: String
  $after: String
  $first: Int
  $last: Int
  $filters: HardwareFilters
) {
  hardwareList(
    before: $before
    after: $after
    first: $first
    last: $last
    filters: $filters
  ) {
    totalCount
    edges {
      cursor
      node {
        ...HardwareFragment
      }
    }
  }
}
"""
)

hardware_ssh_credentials = """
query hardwareSSHCredentials($id: GlobalID!) {
  hardware(id: $id) {
    id
    pk
    sshCredentials
  }
}
"""
