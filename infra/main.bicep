targetScope = 'subscription'

param location string
param acrName string
param rgName string

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgName
  location: location
}

module acr './acr.bicep' = {
  name: 'resourcesModule'
  scope: resourceGroup
  params: {
    location: location
    acrName: acrName
  }
}
