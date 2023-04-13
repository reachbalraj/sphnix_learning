.. _plantUml:

.. sectnum:: 

Plant UML diagrams
==================

activity diagrams
-----------------

.. uml::

    start 

        : Get Started;
        : doing;

    stop

sequence diagrams
-----------------
.. uml:: 

   Alice -> Bob: Hi!
   Alice <- Bob: How are you?


.. uml::
   
   @startuml 
   Alice -> Bob: Hi!
   Alice <- Bob: How are you?
   @enduml

class diagrams
-----------------
.. uml::

      @startuml
      
      'style options 
      skinparam monochrome true
      skinparam circledCharacterRadius 0
      skinparam circledCharacterFontSize 0
      skinparam classAttributeIconSize 0
      hide empty members
      
      Class01 <|-- Class02
      Class03 *-- Class04
      Class05 o-- Class06
      Class07 .. Class08
      Class09 -- Class10
      
      @enduml

use case diagrams
-------------------
.. uml:: 

    left to right direction

    actor Alice
    actor Bob

    rectangle "System" {

    usecase (Use case A) as ucA
    usecase (Use case B) as ucB
    usecase (Use case AB) as ucAB
    
    }

    Alice -- ucA
    Bob -- ucB

    ucB -- Bob 
    ucAB -- Bob 

state machine
--------------

.. uml:: 

    
    state NormalOperation{
        state Uninit
        state Stopped
        state Started

        [*] -> Uninit
        Uninit -> Stopped: Init()
        Stopped -> Started: Start()
        Started -> Stopped: Stop()
        Stopped -> Uninit: DeInit()
    }
    
    [*] -> NormalOperation