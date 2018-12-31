resource azurerm_kubernetes_cluster "aks" {
  name                = "FXWEPOCAKS01"
  resource_group_name = "${azurerm_resource_group.RG03.name}"
  location            = "${azurerm_resource_group.RG03.location}"

  dns_prefix = "FXWEPOCAKS01"

  agent_pool_profile {
    name            = "agentpool"
    count           = 3
    vm_size         = "Standard_DS2_v2"
    os_type         = "Linux"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = "e2e48dfb-7261-4372-9d7a-b20c61059231" #"00000000-0000-0000-0000-000000000000"  
    client_secret = ""                                     #"00000000000000000000000000000000"
  }
}
