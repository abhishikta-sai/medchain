const Admin = artifacts.require("Admin");
const Manufacture = artifacts.require("Manufacture");
const Manufacture1 = artifacts.require("Manufacture1");
const Manufacture2 = artifacts.require("Manufacture2");
const Wholesaler = artifacts.require("Wholesaler");

module.exports = function(deployer) {
  deployer.deploy(Admin).then(function(){
    return deployer.deploy(Manufacture, Admin.address,1);
  }).then(function(){
    return deployer.deploy(Manufacture1, Admin.address,2);
  }).then(function(){
    return deployer.deploy(Manufacture2, Admin.address,3);
  }).then(function(){
    return deployer.deploy(Wholesaler, Admin.address,Manufacture.address,Manufacture1.address,Manufacture2.address,2);
  });
  
}