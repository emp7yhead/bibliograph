import React from 'react';
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button } from '@nextui-org/react';

export default function AppNavbar() {
  return (
    <Navbar isBordered shouldHideOnScroll>
      <NavbarBrand>
        <p className="font-bold text-inherit">bibliograph</p>
      </NavbarBrand>
      <NavbarContent className="sm:flex gap-4" justify="center">
        <NavbarItem>
          <Button as={Link} radius="full" color="primary" href="#" variant="bordered">
            Books
          </Button>
        </NavbarItem>
        <NavbarItem isActive>
          <Button as={Link} radius="full" color="primary" href="#" variant="bordered">
            Bookshelves
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} radius="full" color="primary" href="#" variant="bordered">
            Statistic
          </Button>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="lg:flex">
          <Button as={Link} radius="full" color="primary" href="#" variant="bordered">
            Log in
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} radius="full" color="primary" href="#" variant="flat">
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
