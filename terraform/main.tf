
provider "azurerm" {

  subscription_id = "" # enter your subscription id

  features {}

}



# Resource Group

resource "azurerm_resource_group" "rg" {

  name     = "" # name of your resource group

  location = "eastus"

}

# Azure Container Registry

resource "azurerm_container_registry" "acr" {

  name                     = "azure2deploy" #name of my existing container registry

  location                 = "eastus"

  resource_group_name      = azurerm_resource_group.rg.name

  sku                      = "Basic"

  admin_enabled            = true

  public_network_access_enabled = true

  tags = {

    environment = "Development"

  }

}



# Public IP for external access

resource "azurerm_public_ip" "public_ip" {

  name                         = "fire-detection-container-ip"

  resource_group_name          = azurerm_resource_group.rg.name

  location                     = azurerm_resource_group.rg.location

 allocation_method   = "Static"  

  sku                 = "Standard"

}



# Container Group

resource "azurerm_container_group" "container" {

  name                        = "fire-detection-container"

  location                    = azurerm_resource_group.rg.location

  resource_group_name         = azurerm_resource_group.rg.name

  os_type                     = "Linux"

  restart_policy              = "Always"

  sku                         = "Standard"

  tags = {

    environment = "Development"

  }



  container {

    name      = "detection"

    image     = "azure2deploy.azurecr.io/welcome:latest"

    cpu       = 0.5

    memory    = 1.5



    ports {

      port     = 80

      protocol = "TCP"

    }

  }



  image_registry_credential {

    username = azurerm_container_registry.acr.admin_username  # Use the admin username from the ACR

    password = azurerm_container_registry.acr.admin_password  # Use the admin password from the ACR

    server   = "azure2deploy.azurecr.io"

  }





}



# Push Image (using local-exec provisioner)

resource "null_resource" "push_image" {

  provisioner "local-exec" {

    command = <<EOT

      docker login azure2deploy.azurecr.io -u ${azurerm_container_registry.acr.admin_username} -p ${azurerm_container_registry.acr.admin_password}

      docker tag image_name azure2deploy.azurecr.io/image_name:latest

      docker push azure2deploy.azurecr.io/image_name:latest

    EOT

  }



  depends_on = [azurerm_container_registry.acr]

}
