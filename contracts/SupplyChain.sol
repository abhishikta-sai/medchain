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
        string man_name;
        uint med_id;
        uint quantity;
        bytes32 batchNo;
        uint licenseMan;
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

    function addRecordToTable(address _manufacturer,string memory _man_name, uint _med_id,uint _quantity,uint _licenseMan,bytes32 _batchNo) public{
        require(licenseMans[_licenseMan] == true, "Invalid Manufacture License");
        recordCount += 1;
        records[recordCount] = Record(recordCount,_manufacturer,_man_name,_med_id,_quantity,_batchNo,_licenseMan,medName,manDate,expDate);
        hashedaccess = keccak256(abi.encodePacked(_manufacturer,_med_id));
        getrecids[hashedaccess] = recordCount;
    }

    function addManufactureRecord(address _manufacturer,string calldata _man_name,uint _med_id,uint _quantity,uint _licenseMan, string calldata _medName,string calldata _manDate,string calldata _expDate) external returns(bytes32){
        uint tempSecretx = block.timestamp;
        bytes32 batchNo = keccak256(abi.encodePacked(_manufacturer,_med_id,_quantity, tempSecretx));
        manDate = _manDate;
        medName = _medName;
        expDate = _expDate;
        addRecordToTable(_manufacturer,_man_name,_med_id,_quantity,_licenseMan,batchNo);
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
        addRecordToTable(_wholesaler,"wholesaler",_med_id,_quantity,_license,records[getrecids[hashedaccess]].batchNo);
        return records[getrecids[hashedaccess]].batchNo ;
    }
    
    function validate(address _wholesaler,uint _med_id,bytes32 _batchNo) external returns(bool){
        hashedaccess = keccak256(abi.encodePacked(_wholesaler,_med_id));
        return records[getrecids[hashedaccess]].batchNo == _batchNo ; 
    }
}


contract Manufacture{
    address public Owner;
    address Adminaddress;
    address public using_address;
    bytes32 public batchNo;
    uint public license;
    constructor(address _admin,uint _licenseMan) public {
        Adminaddress = _admin;
        Owner = msg.sender;
        using_address = address(this);
        license = _licenseMan;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }

    function addMedicineRecord(string memory _man_name,uint _med_id,uint _quantity,string memory _medName,string memory _manDate,string memory _expDate) public onlyOwner returns(bytes32){
    Admin adminConnect = Admin(Adminaddress);
    batchNo = adminConnect.addManufactureRecord(using_address,_man_name,_med_id,_quantity,license,_medName,_manDate,_expDate);
    return batchNo;
    }
    
    function sellMedicine (address _wholesaler, uint _med_id, uint _quantity, uint _license) external returns(bytes32){
        Admin adminConnect = Admin (Adminaddress);
        return adminConnect.WholesalerTransaction(using_address,_wholesaler,_med_id,_quantity,_license);
        
    }
}

contract Manufacture1{
    address public Owner;
    address Adminaddress;
    address public using_address;
    bytes32 public batchNo;
    uint public license;
    constructor(address _admin,uint _licenseMan) public {
        Adminaddress = _admin;
        Owner = msg.sender;
        using_address = address(this);
        license = _licenseMan;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }

    function addMedicineRecord(string memory _man_name,uint _med_id,uint _quantity,string memory _medName,string memory _manDate,string memory _expDate) public onlyOwner returns(bytes32){
    Admin adminConnect = Admin(Adminaddress);
    batchNo = adminConnect.addManufactureRecord(using_address,_man_name,_med_id,_quantity,license,_medName,_manDate,_expDate);
    return batchNo;
    }
    
    function sellMedicine (address _wholesaler, uint _med_id, uint _quantity, uint _license) external returns(bytes32){
        Admin adminConnect = Admin (Adminaddress);
        return adminConnect.WholesalerTransaction(using_address,_wholesaler,_med_id,_quantity,_license);
        
    }
}

contract Manufacture2{
    address public Owner;
    address Adminaddress;
    address public using_address;
    bytes32 public batchNo;
    uint public license;
    constructor(address _admin,uint _licenseMan) public {
        Adminaddress = _admin;
        Owner = msg.sender;
        using_address = address(this);
        license = _licenseMan;
    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }

    function addMedicineRecord(string memory _man_name,uint _med_id,uint _quantity,string memory _medName,string memory _manDate,string memory _expDate) public onlyOwner returns(bytes32){
    Admin adminConnect = Admin(Adminaddress);
    batchNo = adminConnect.addManufactureRecord(using_address,_man_name,_med_id,_quantity,license,_medName,_manDate,_expDate);
    return batchNo;
    }
    
    function sellMedicine (address _wholesaler, uint _med_id, uint _quantity, uint _license) external returns(bytes32){
        Admin adminConnect = Admin (Adminaddress);
        return adminConnect.WholesalerTransaction(using_address,_wholesaler,_med_id,_quantity,_license);
        
    }
}

contract Wholesaler{
    string public medicines;
    mapping(uint => address) man_address;
    address public Owner;
    address Adminaddress;
    bool public done;
    address usingAddress;
    uint license;
    constructor(address _admin,address _man1,address _man2,address _man3, uint _license) public{
        medicines = "Paracetamol";
        Adminaddress = _admin;
        Owner = msg.sender;
        license = _license;
        man_address[0] = _man1;
        man_address[1] = _man2;
        man_address[2] = _man3;
        usingAddress = address(this);

    }
    modifier onlyOwner() {
        require(msg.sender == Owner, "Only owner can call this function");
        _;
    }
    function validate(uint _med_id,bytes32 _batchNo) private returns (bool) {
        Admin adm = Admin(Adminaddress);
        return adm.validate(usingAddress,_med_id,_batchNo);
    }
    function buyMedicine(uint _index, uint _med_id, uint _quantity) public onlyOwner{
        Manufacture Man = Manufacture(man_address[_index]);
        bytes32 hashedaccess = Man.sellMedicine(usingAddress,_med_id,_quantity,license);
        done = validate(_med_id,hashedaccess);
    }
}