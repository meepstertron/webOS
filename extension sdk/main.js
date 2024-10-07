class webOSHelpers {
    getInfo() {
        return {
            id: "weboshelpers",
            name: "WebOS Helper Blocks",
            blocks: [
                {
                    opcode: "getVersion",
                    blockType: Scratch.BlockType.REPORTER,
                    text: "get WebOS version",
                },
                {
                    opcode: "getIfOnWebOS",
                    blockType: Scratch.BlockType.BOOLEAN,
                    text: "is on WebOS?",
                },
                {
                    opcode: "getStat",
                    blockType: Scratch.BlockType.REPORTER,
                    text: "get [STAT] WebOS stat",
                    arguments: {
                        STAT: {
                            type: Scratch.ArgumentType.STRING,
                            menu: 'STATS_MENU'
                        }
                    }

                },
                {
                    opcode: "shutdown",
                    blockType: Scratch.BlockType.COMMAND,
                    text: "Shutdown",
                },
                {
                    opcode: "restart",
                    blockType: Scratch.BlockType.COMMAND,
                    text: "Restart",
                },
                {
                    opcode: "runSSHCommand",
                    blockType: Scratch.BlockType.REPORTER,
                    text: "Run SSH Command [COMMAND] at [ADDRESS] as [USERNAME] with [PASSWORD]",
                    arguments: {
                        COMMAND: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'echo hi'
                        },
                        ADDRESS: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'localhost'
                        },
                        USERNAME: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'root'
                        },
                        PASSWORD: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'password'
                        }
                    }

                },
            ],
            menus: {
                STATS_MENU: {
                    acceptReporters: true,
                    items: [
                        {
                            text: 'CPU Percentage',
                            value: 'cpu'
                        },
                        {
                            text: 'Memory usage Percentage',
                            value: 'ram'
                        },
                        {
                            text: 'Disk Usage',
                            value: 'disk'
                        },
                        {
                            text: 'Network Connections',
                            value: 'network'
                        },
                        {
                            text: 'Computer Name',
                            value: 'name'
                        },
                        {
                            text: 'OS Platform',
                            value: 'platform'
                        },
                        {
                            text: 'Architecture',
                            value: 'machine'
                        }
                        
                    ]
                }
            }
        };
    }

    async runSSHCommand(args) {
        const data = {
          host: args.ADDRESS,
          username: args.USERNAME,
          password: args.PASSWORD,
          command: args.COMMAND
        };
      
        try {
          const response = await fetch("http://127.0.0.1:8080/run-command", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
          });
      
          if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
          }
      
          const result = await response.json();
          console.log("Output:", result.output);
          return(result.output)
        } catch (error) {
          console.error("There was a problem with the fetch operation:", error);
          return("Error")
        }
      }
      
      
      
      

    async shutdown() {
        const response = await fetch("http://127.0.0.1:8080/shutdown"); 
    }

    async restart() {
        const response = await fetch("http://127.0.0.1:8080/restart");
    }

    async getStat(args) {
        try {
            const response = await fetch("http://127.0.0.1:8080/systeminfo");
    
            // Check if the request was successful
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
    
            // Parse the JSON from the response
            const data = await response.json();
    
            // Access the stat from the JSON data using the correct argument name
            console.log(args.STAT);
            const statValue = data[args.STAT];
            console.log("Fetched WebOS stat:", statValue);
    
            return statValue;
        } catch (error) {
            console.error("Error fetching WebOS stat:", error);
            return "Error"; // Return a fallback error message
        }
    }
    

    async getIfOnWebOS() {
        try {
            const response = await fetch("http://127.0.0.1:8080/systeminfo");

            // Check if the request was successful
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            // Parse the JSON from the response
            const data = await response.json();

            // Access the version from the JSON data
            const version = data["version"];
            console.log("Fetched WebOS version:", version);

            return true; // Return the version as a string
        } catch (error) {
            console.error("Error fetching WebOS version:", error);
            return false; // Return a fallback error message
        }
    }


    // Mark the function as async to handle asynchronous code
    async getVersion() {
        try {
            const response = await fetch("http://127.0.0.1:8080/systeminfo"); // Replace with your API URL

            // Check if the request was successful
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            // Parse the JSON from the response
            const data = await response.json();

            // Access the version from the JSON data
            const version = data["version"];
            console.log("Fetched WebOS version:", version);

            return version; // Return the version as a string
        } catch (error) {
            console.error("Error fetching WebOS version:", error);
            return "Error"; // Return a fallback error message
        }
    }
}

// Register the extension with TurboWarp
Scratch.extensions.register(new webOSHelpers());
