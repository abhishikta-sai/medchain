//var SupplyChain = artifacts.require("./SupplyChain.sol");
/*
module.exports = function(deployer) {
  deployer.deploy(Admin);
  deployer.deploy(Manufacture);
};
*/

const Admin = artifacts.require("Admin");
const Manufacture = artifacts.require("Manufacture");
const Wholesaler = artifacts.require("Wholesaler");
const Customer = artifacts.require("Customer");

module.exports = function(deployer) {
  deployer.deploy(Admin).then(function(){
    return deployer.deploy(Manufacture, Admin.address,1);
  }).then(function(){
    return deployer.deploy(Wholesaler, Admin.address,2);
  }).then(function(){
    return deployer.deploy(Customer, Admin.address);
  });
  
}