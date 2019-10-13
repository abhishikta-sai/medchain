pragma solidity ^0.5.0;

contract Admin{
    uint public recordCount = 0;
    bytes32 public hashedaccess;
    string medName;
    string manDate;
    string expDate;
    struct Record {
        uint Recid;
        address manufacturer;
        uint med_id;
        uint quantity;
        bytes32 batchNo;
        uint licenseMan;
        uint licenseWhole;
        string medName;
        string manDate;
        string expDate;
    }

    mapping(uint => Record) public records;
    mapping(uint => bool) public licenseMans;
    mapping(uint => bool) public licenseWho;
    mapping(bytes32 => uint) public getrecids;
    constructor() public {
        licenseMans[1] = true;
        licenseMans[2] = true;
        licenseMans[3] = true;
        
        licenseWho[1] = true;
        licenseWho[2] = true;
        licenseWho[3] = true;
    }

    function addRecordToTable(address _manufacturer,uint _med_id,uint _quantity,uint _licenseMan,uint _licensewho,bytes32 _batchNo) public{
        if(_licensewho == 0){
        require(licenseMans[_licenseMan] == true, "Invalid Manufacture License");}
        else{
        require(licenseWho[_licensewho] == true, "Invalid Wholesaler License");
        }//recordCount = recordCount + 1;
        recordCount += 1;
        records[recordCount] = Record(recordCount,_manufacturer,_med_id,_quantity,_batchNo,_licenseMan,_licensewho,medName,manDate,expDate);
        hashedaccess = keccak256(abi.encodePacked(_manufacturer,_med_id));
        getrecids[hashedaccess] = recordCount;
    }

    function addManufactureRecord(address _manufacturer,uint _med_id,uint _quantity,uint _licenseMan,uint _licenseWho, string calldata _medName,string calldata _manDate,string calldata _expDate) external returns(bytes32){
        uint tempSecretx = block.timestamp;
        bytes32 batchNo = keccak256(abi.encodePacked(_manufacturer,_med_id,_quantity, tempSecretx));
        manDate = _manDate;
        medName = _medName;
        expDate = _expDate;
        addRecordToTable(_manufacturer,_med_id,_quantity,_licenseMan,_licenseWho,batchNo);
        return batchNo;
    }
    function WholesalerTransaction(address _manufacturer,address _wholesaler,uint _med_id,uint _quantity,uint _license) external returns(bytes32){
        hashedaccess = keccak256(abi.encodePacked(_manufacturer,_med_id));
        
        uint test1 = getrecids[hashedaccess];
        uint test = records[test1].quantity;
        require( test >= _quantity,"Medicines are out of stock");
        records[getrecids[hashedaccess]].quantity -= _quantity;
        manDate = records[test1].manDate;
        medName = records[test1].medName;
        expDate = records[test1].expDate;
        addRecordToTable(_wholesaler,_med_id,_quantity,0,_license,records[getrecids[hashedaccess]].batchNo);
        return records[getrecids[hashedaccess]].batchNo ;
    }
    
    function validate(address _wholesaler,uint _med_id,bytes32 _batchNo) external returns(bool){
        hashedaccess = keccak256(abi.encodePacked(_wholesaler,_med_id));
        return records[getrecids[hashedaccess]].batchNo == _batchNo ; 
    }
    
    function getnumberofWholsaleDealers(uint _med_id) external view returns(uint){
        uint num=0;
        for(uint i=1;i<=recordCount;i++){
            if(records[i].licenseMan == 0)
            num=num+1;
        }
        return num;
    }
    
    function getWholeSale(uint _i) external view returns(uint,address,uint,string memory){
        for(uint i=_i;i<=recordCount;i++){
            if(records[i].licenseWhole != 0)
            return (1,records[i].manufacturer,records[i].quantity,records[i].medName);
        }
        return(0,records[0].manufacturer,records[0].quantity,records[0].medName);
    }
}


contract Manufacture{
    string public medicines;
    address public Owner;
    address Adminaddress;
    uint license;
    constructor(address _admin,uint _licenseMan) public {
        medicines = "Paracetamol";
        Adminaddress = _admin;
        Owner = msg.sender;
        license = _licenseMan;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }

    function addMedicineRecord(uint _med_id,uint _quantity,string memory _medName,string memory _manDate,string memory _expDate) public onlyOwner{
    Admin adminConnect = Admin(Adminaddress);
    bytes32 batchNo = adminConnect.addManufactureRecord(msg.sender,_med_id,_quantity,license,0,_medName,_manDate,_expDate);
    }
    
    function sellMedicine (address _wholesaler, uint _med_id, uint _quantity, uint _license) external returns(bytes32){
        Admin adminConnect = Admin (Adminaddress);
        return adminConnect.WholesalerTransaction(Owner,_wholesaler,_med_id,_quantity,_license);
        
    }
    
    
}

contract Wholesaler{
    string public medicines;
    address public Owner;
    address Adminaddress;
    uint license;
    constructor(address _admin, uint _license) public{
        medicines = "Paracetamol";
        Adminaddress = _admin;
        Owner = msg.sender;
        license = _license;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }
    function validate(uint _med_id,bytes32 _batchNo) private {
        Admin adm = Admin(Adminaddress);
        require(adm.validate(msg.sender,_med_id,_batchNo),"Unsuccessfull Transaction");
    }
    function buyMedicine (address _manufacturer , uint _med_id,uint _quantity) public onlyOwner{
        Manufacture Man = Manufacture(_manufacturer);
        bytes32 hashedaccess = Man.sellMedicine(msg.sender,_med_id,_quantity,license);
        validate(_med_id,hashedaccess);
    }
}

contract Customer{
    address public Owner;
    address Adminaddress;
    uint i=1;
    constructor(address _admin) public{
        Adminaddress = _admin;
        Owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }
    
    event wholesalerFound(address _wholesaler,uint _quantity,string medName);
    
    function getMedicines(uint _med_id) public onlyOwner{
        Admin adm = Admin(Adminaddress);
        uint num = adm.getnumberofWholsaleDealers(_med_id);
        while(i<=num){
            (uint a,address b,uint c,string memory d) = adm.getWholeSale(i);
            if(a==0)
            break;
            i = i+1;
            emit wholesalerFound(b,c,d);
            
        }
        i=1;
        
    }
}
