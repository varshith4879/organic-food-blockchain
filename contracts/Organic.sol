// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 <= 0.9.0;

contract Organic {
    string public farmer;
    string public distributor;
    string public retailer;
    string public customer;
    string public users;

    function setfarmer(string memory ud) public {
        farmer = ud;	
    }

    function getfarmer() public view returns (string memory) {
        return farmer;
    }

    function setdistributor(string memory pd) public {
        distributor = pd;	
    }

    function getdistributor() public view returns (string memory) {
        return distributor;
    }

    function setretailer(string memory ra) public {
        retailer = ra;	
    }

    function getretailer() public view returns (string memory) {
        return retailer;
    }

    function setcustomer(string memory ca) public {
        customer = ca;	
    }

    function getcustomer() public view returns (string memory) {
        return customer;
    }
    
    function setuser(string memory pa) public {
        users = pa;	
    }

    function getuser() public view returns (string memory) {
        return users;
    }

    constructor() public {
    farmer = "";
	distributor = "";
    retailer = "";
    customer = "";
    users = "";
    }
}