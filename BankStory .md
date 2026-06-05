Use Case : Banking System Requirements - A Story
A modern bank requires a simple but robust account management system to serve its customers effectively. The bank's customers have specific needs and expectations that the system must fulfill through reliable and secure banking operations.

THE ACCOUNT CREATION STORY

When a new customer comes to the bank, they want to open an account with an initial deposit. The system should create an account with their opening balance and automatically set up some basic parameters. Every new account starts with a minimum balance requirement of 500 rupees, an overdraft facility of 500 rupees, and an "Active" status, giving customers confidence that their account is ready for transactions.

THE WITHDRAWAL STORY

A bank customer approaches an ATM to withdraw money for their expenses. They expect the system to check several things before allowing their withdrawal:
- First, the system should verify that her account is not closed, because closed accounts cannot perform any transactions
- Second, it should ensure she doesn't withdraw more than her available balance plus her overdraft limit
- If she has enough money in her account, the system should simply deduct the amount from her current balance
- However, if her account balance is insufficient but she has overdraft available, the system should use her remaining balance first, then tap into her overdraft facility
- After every withdrawal, the system should automatically reassess her account status to ensure it reflects her current financial standing

THE DEPOSIT STORY
When a customer receives their salary and wants to deposit it into their account, the system should handle this transaction intelligently:
- The system must first verify that their account is not closed
- If the customer has been using their overdraft facility (meaning they owe money to the bank), the system should prioritize paying back the overdraft before adding money to their available balance
- Once the overdraft is fully repaid (back to the standard 500 rupees), any remaining deposit amount should be added to their account balance
- After the deposit, the system should update their account status to reflect their improved financial position

THE ACCOUNT STATUS STORY
The bank wants to automatically manage account statuses based on customer behavior and account conditions:

ACTIVE ACCOUNTS: Customers with balances above the minimum requirement (500 rupees) enjoy full banking privileges with an "Active" status.

OVERDUE ACCOUNTS: When customers use their overdraft facility (overdraft amount drops below 500), their account becomes "Overdue," signaling that they owe money to the bank.

SUSPENDED ACCOUNTS: If customers completely exhaust their overdraft facility (overdraft reaches 0), their account becomes "Suspended," indicating a more serious financial situation.

CLOSED ACCOUNTS: When an account's financial situation becomes untenable (balance falls below minimum plus overdraft obligations), the account automatically closes to protect both the bank and the customer from further financial complications.

THE BALANCE INQUIRY STORY
Customers should be able to check their account balance at any time, receiving accurate, real-time information about their available funds.

THE STATUS MONITORING STORY
The system should provide transparency by allowing customers and bank staff to check the current status of any account, helping everyone understand the account's standing and available services.

THE BUSINESS RULES STORY
Behind the scenes, the system follows strict business logic:
- Account transitions between statuses are governed by specific financial thresholds
- The system prevents unauthorized transactions on closed accounts
- Overdraft facilities are managed automatically based on customer usage
- Account status changes are immediate and reflect real-time account conditions

This banking system story ensures that customers can manage their money safely while the bank maintains appropriate risk management and regulatory compliance through automated account status monitoring and transaction controls.
