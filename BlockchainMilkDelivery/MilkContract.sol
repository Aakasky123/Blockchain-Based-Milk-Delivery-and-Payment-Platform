pragma solidity >= 0.8.11 <= 0.8.11;

contract MilkContract {
    string public nadafa_users;
    string public farmer_milk_delivery;

    function addNadafaStaff(string memory ns) public {
        nadafa_users = ns;	
    }

    function getNadafaStaff() public view returns (string memory) {
        return nadafa_users;
    }

    function addMilkDelivery(string memory fm) public {
        farmer_milk_delivery = fm;	
    }

    function getMilkDelivery() public view returns (string memory) {
        return farmer_milk_delivery;
    }

    constructor() public {
        nadafa_users = "empty";
	farmer_milk_delivery = "empty";
    }
}