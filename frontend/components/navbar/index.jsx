import React from 'react';
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button, Divider } from '@nextui-org/react';

export default function AppNavbar() {
  return (
    <Navbar>
      <NavbarBrand>
        <p className="font-bold text-inherit">BIBLIOgraph</p>
      </NavbarBrand>
      <NavbarContent className="sm:flex gap-4" justify="center">
        <NavbarItem>
          <Link color="black" href="#">
            Books
          </Link>
        </NavbarItem>
        <Divider orientation="vertical" />
        <NavbarItem isActive>
          <Link href="#" color="black" aria-current="page">
            Bookshelves
          </Link>
        </NavbarItem>
        <Divider orientation="vertical" />
        <NavbarItem>
          <Link color="black" href="#">
            Statistic
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="lg:flex">
          <Link href="#">Login</Link>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} color="primary" href="#" variant="flat">
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
