terraform {
  backend "azurerm" {
    resource_group_name  = "exam-reminder-rg"
    storage_account_name = "examremindertfstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}